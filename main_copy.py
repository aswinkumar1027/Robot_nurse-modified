import tornado.ioloop
import tornado.web

import datetime
import gpiozero
import time
import serial
import subprocess
import os


robot = gpiozero.Robot(left=(26,16), right=(5,6))

leftend = gpiozero.DigitalInputDevice(17)
center = gpiozero.DigitalInputDevice(27)
rightend = gpiozero.DigitalInputDevice(22)
leftback = gpiozero.DigitalInputDevice(23)
rightback = gpiozero.DigitalInputDevice(19)

thermal = gpiozero.LED(20)
pressures = gpiozero.LED(21)

rfid_dict = {'E235FC8B\r\n': 'A1'}
active_beds = ('A1')                                        #fetch from main server
left_beds = ('A1')

ser=serial.Serial("/dev/ttyACM0",9600)  #change ACM number as found from ls /dev/tty/ACM*
ser.baudrate = 9600

turn_left = False

def line_follow_config(fn):
    leftend.when_activated = fn
    rightend.when_activated = fn
    center.when_activated = fn
    leftback.when_activated = fn
    rightback.when_activated = fn


    leftend.when_deactivated = fn
    rightend.when_deactivated = fn
    center.when_deactivated = fn
    leftback.when_deactivated = fn
    rightback.when_deactivated = fn

    
    

def rfid_read():
    global turn_left                                   #rfid taking and decisions
    print("RFID")
    read_ser=ser.readline()
    print(read_ser)
    bed = rfid_dict[read_ser]
    
    if (bed in active_beds):
        print("Active beds are detected")
        turn_left = bed in left_beds
        turn_robot()
    else:
        print("not in active beds list")
        # So that robot automatically moves on to next bed
        robot.forward()
        time.sleep(1)
        line_follow()

        
def turn_robot():
    if turn_left:                                  #interaction left turning
        print("turning_left")
        robot.left()
        time.sleep(0.7)
    else:
        print("turning_right")
        robot.right()
        time.sleep(0.7)
    while True:
        if center.is_active:
            robot.stop()
            break


def examine():
    global turn_left                                        #examination_finish and continue
    turn_left = not turn_left
    turn_robot()
    #follow_line()



# def follow_line():                                        #line_follower main code
#     while True:
#         p = subprocess.Popen(['python', 'line_detect.py'])
#         #(output, err) = p.communicate()
#         p_status = p.wait()
#         print("condition met")
#         print(p_status)
#         rfid_read()


def check():
    if leftback.is_active and rightback.is_active:
        print("Junction stop")
        robot.stop()
        line_follow_config(None)
        rfid_read()
    
    elif center.is_active and leftend.is_active and rightend.is_active:
        print("near_junction")
        robot.forward()
        time.sleep(0.5)
        

    elif center.is_active and (not leftend.is_active) and (not rightend.is_active):
        print("forward")
        robot.forward()
    elif (not leftend.is_active) and rightend.is_active:
        robot.right()
        print("right")
    elif leftend.is_active and (not rightend.is_active):
        robot.left()
        print("left")





def line_follow():
    line_follow_config(check)
    check()



def take_pressure():                                      #pressure taking button
    pressures.on()
    time.sleep(0.5)
    pressures.off()

robo_actions = {
    "forward": robot.forward,
    "backward": robot.backward,
    "left": robot.left,
    "right": robot.right,
    "stop": robot.stop,
    "line": line_follow,
    "examine": examine,
    "pressure": take_pressure,
    "Temperature": thermal.on
}

    


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("main.html")

class CommandHandler(tornado.web.RequestHandler):
    def post(self):
        movement = self.get_body_argument("movement")
        robo_actions[movement]()
        self.write("You wrote " + movement)

settings = dict(
	template_path = os.path.join(os.path.dirname(__file__), "templates"),
	static_path = os.path.join(os.path.dirname(__file__), "static")
	)

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/move", CommandHandler),
    ], **settings)

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
import tornado.ioloop
import tornado.web
import RPi.GPIO as GPIO
import datetime
import gpiozero
import time
import serial
import subprocess
import os



robot = gpiozero.Robot(left=(11,25), right=(9,10))

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

ser=serial.Serial("/dev/ttyACM1",9600)  #change ACM number as found from ls /dev/tty/ACM*
ser.baudrate = 9600

turn_left = False
line_follow_mode = False

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

    
def stop_line_follow():
    global line_follow_mode
    line_follow_mode = False
    print("pressed_stop")
    robot.stop()
    
    

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
        print("not active_bed")
        # So that robot automatically moves on to next bed
        robot.forward()
        time.sleep(1)
        line_follow()

        
def turn_robot():
    if turn_left:                                  #interaction left turning
        print("turning_left")
        robot.left()
    else:
        print("turning_right")
        robot.right()
    time.sleep(1)
    while True:
        if center.is_active:
            print("center_active")
            time.sleep(0.4)
            print("time_implemented")   #implement timne delay
            robot.stop()
            print("robot_stopped")
            break



    



# def follow_line():                                        #line_follower main code
#     while True:
#         p = subprocess.Popen(['python', 'line_detect.py'])
#         #(output, err) = p.communicate()
#         p_status = p.wait()
#         print("condition met")
#         print(p_status)
#         rfid_read()


def check():
    while True:
        print(center.is_active , leftend.is_active , rightend.is_active, leftback.is_active , rightback.is_active)
        if not line_follow_mode:
            robot.stop()
            print("not_line follow mode")
            break

        elif leftback.is_active and rightback.is_active:
            print("Junction stop")
            robot.stop()
            stop_line_follow()
            rfid_read()
        
        #elif center.is_active and leftend.is_active and rightend.is_active:
         #   print("near_junction")
          #  robot.forward()
           # time.sleep(0.2)
            

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
    print("line_follow")

    global line_follow_mode
    line_follow_mode = True
    check()


#line_follow_config(check)

def examine():
    global turn_left                                        #examination_finish and continue
    turn_left = not turn_left
    turn_robot()
    robot.forward()
    print("forward_after turn")
    time.sleep(1.3)
    print("line_follow_started")
    line_follow()

def stop_robot():
    robot.stop()
    stop_line_follow()


def take_pressure():                                      #pressure taking button
    pressures.on()
    time.sleep(0.5)
    pressures.off()

robo_actions = {
    "forward": robot.forward,
    "backward": robot.backward,
    "left": robot.left,
    "right": robot.right,
    "stop": stop_line_follow,
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

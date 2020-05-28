from flask import Flask, render_template, request
import datetime
import gpiozero
import time

app = Flask(__name__)
robot = gpiozero.Robot(left=(26,16), right=(5,6))

leftend = gpiozero.DigitalInputDevice(17)
center = gpiozero.DigitalInputDevice(27)
rightend = gpiozero.DigitalInputDevice(22)
leftback = gpiozero.DigitalInputDevice(23)
rightback = gpiozero.DigitalInputDevice(19)

thermal = gpiozero.LED(20)
pressures = gpiozero.LED(21)

rfid_dict = {}
active_beds = ()                                        #fetch from main server
left_beds = []

global turn_var = 0




def rfid_read():                                       #rfid taking and decisions
    print("RFID")
    read_ser=ser.readline()
    print(read_ser)
    bed = rfid_dict(read_ser)
    if (bed in active_beds):
        print("Active beds are detected")
        if (bed in left_beds):
            print("left_turn")
            left_inter(True)
            turn_var = 1
            break
        else:
            right_inter(True)
            print("right_turn")
            turn_var = 2
            break
    else:
        print("not in active beds list")

        
        

            


def left_inter():                                       #interaction left turning
    robot.left()
    time.sleep(0.5)
    while True:
        if (center.is_active = True):
            robot.stop
            break



def right_inter():                                      #interaction right turning
    robot.right()
    time.sleep(0.5)
    while True:
        if (center.is_active = True):
            robot.stop
            break



def examine():                                          #examination_finish and continue
    if(turn_var == 1):
        right_inter()
        print("turning_right")
    elif:
        turn_var == 2:
        left_inter()
        print("turning_left")
    
    follow_line()



def follow_line():                                        #line_follower main code
    global mode
    while True:
        p = subprocess.Popen(['python', 'line_detect.py'])
        #(output, err) = p.communicate()
        p_status = p.wait()
        print("condition met")
        print(p_status)
        rfid_read()






def take_pressure():                                      #pressure taking button
    pressures.on()
    pressures.off()




robo_actions = {
    "forward": robot.forward,
    "backward": robot.backward,
    "left": robot.left,
    "right": robot.right,
    "stop": robot.stop,
    "line": follow_line,
    "examine": examine,
    "pressure": take_pressure,
    "Temperature": thermal.on
}

@app.route("/")                   
def hello():                      
    return render_template('main.html')

@app.route("/move", methods=['GET', 'POST'])                   
def move():
    movement = request.form['movement']
    robo_actions[movement]()
    return "Moving " + movement
    
if __name__ == "__main__":        
    app.run(host='0.0.0.0', debug=True)

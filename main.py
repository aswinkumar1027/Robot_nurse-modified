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
left_beds = ()

turn_left = False

def rfid_read():
    global turn_var                                   #rfid taking and decisions
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
        follow_line()

        
def turn_robot():
    if turn_left:                                  #interaction left turning
        print("turning_left")
        robot.left()
    else:
        print("turning_right")
        robot.right()
    time.sleep(0.5)
    while True:
        if center.is_active:
            robot.stop()
            break


def examine():
    global turn_left                                        #examination_finish and continue
    turn_left = not turn_left
    turn_robot()
    follow_line()


def follow_line():                                        #line_follower main code
    while True:
        p = subprocess.Popen(['python', 'line_detect.py'])
        #(output, err) = p.communicate()
        p_status = p.wait()
        print("condition met")
        print(p_status)
        rfid_read()


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

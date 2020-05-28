from flask import Flask, render_template, request
import datetime
import gpiozero

app = Flask(__name__)
robot = gpiozero.Robot(left=(26,16), right=(5,6))

leftend = gpiozero.DigitalInputDevice(17)
center = gpiozero.DigitalInputDevice(27)
rightend = gpiozero.DigitalInputDevice(22)
backl = gpiozero.DigitalInputDevice(23)
rightl = gpiozero.DigitalInputDevice(19)

thermal = gpiozero.LED(20)
pressures = gpiozero.LED(21)


def examine():
    pass

def follow_line():
    global mode
    while True:
        if (center.is_active == True) and (leftend.is_active == False) and (rightend.is_active == False):
            print("forward")
            robot.forward()
       
        elif (leftend.is_active == False) and (rightend.is_active == True):
            robot.right()
            print("right")
        elif (leftend.is_active == True) and (rightend.is_active == False):
            robot.left()
            print("left")
        
def take_pressure():
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

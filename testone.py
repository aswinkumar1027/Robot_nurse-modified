import datetime
import gpiozero

#app = Flask(__name__)
robot = gpiozero.Robot(left=(26,16), right=(5,6))

leftend = gpiozero.DigitalInputDevice(17)
center = gpiozero.DigitalInputDevice(27)
rightend = gpiozero.DigitalInputDevice(22)
backl = gpiozero.DigitalInputDevice(23)
rightl = gpiozero.DigitalInputDevice(19) 

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
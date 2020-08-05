import gpiozero
import time

robot = gpiozero.Robot(left=(26,16), right=(5,6))

leftend = gpiozero.DigitalInputDevice(17)
center = gpiozero.DigitalInputDevice(27)
rightend = gpiozero.DigitalInputDevice(22)
leftback = gpiozero.DigitalInputDevice(23)
rightback = gpiozero.DigitalInputDevice(19)


 while True:
        if (leftback.is_active == True) and (rightback == True):
            print("Junction stop")
            robot.stop()
            break

        elif (center.is_active == True) and (leftend.is_active == False) and (rightend.is_active == False):
            print("forward")
            robot.forward()
        elif (leftend.is_active == False) and (rightend.is_active == True):
            robot.right()
            print("right")
        elif (leftend.is_active == True) and (rightend.is_active == False):
            robot.left()
            print("left")
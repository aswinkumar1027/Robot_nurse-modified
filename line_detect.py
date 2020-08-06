import gpiozero
import time

robot = gpiozero.Robot(left=(26,16), right=(5,6))

leftend = gpiozero.DigitalInputDevice(17)
center = gpiozero.DigitalInputDevice(27)
rightend = gpiozero.DigitalInputDevice(22)
leftback = gpiozero.DigitalInputDevice(23)
rightback = gpiozero.DigitalInputDevice(19)


while True:
    if leftback.is_active and rightback:
        print("Junction stop")
        robot.stop()
        break

    elif center.is_active and (not leftend.is_active) and (not rightend.is_active):
        print("forward")
        robot.forward()
    elif (not leftend.is_active) and rightend.is_active:
        robot.right()
        print("right")
    elif leftend.is_active and (not rightend.is_active):
        robot.left()
        print("left")
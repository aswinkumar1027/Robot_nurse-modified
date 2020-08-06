import gpiozero
import time
import sys
from signal import pause
robot = gpiozero.Robot(left=(26,16), right=(5,6))

leftend = gpiozero.DigitalInputDevice(17)
center = gpiozero.DigitalInputDevice(27)
rightend = gpiozero.DigitalInputDevice(22)
leftback = gpiozero.DigitalInputDevice(23)
rightback = gpiozero.DigitalInputDevice(19)


# while True:
#     if leftback.is_active and rightback.is_active:
#         print("Junction stop")
#         robot.stop()
#         break

#     elif center.is_active and (not leftend.is_active) and (not rightend.is_active):
#         print("forward")
#         robot.forward()
#     elif (not leftend.is_active) and rightend.is_active:
#         robot.right()
#         print("right")
#     elif leftend.is_active and (not rightend.is_active):
#         robot.left()
#         print("left")



# def leftend_active():
#     if not rightend.is_active:
#         robot.left()
#         print("left")


# def rightend_active():
#     if not leftend.is_active:
#         robot.right()
#         print("right")


# def center_active():
#     if (not leftend.is_active) and (not rightend.is_active):
#         print("forward")
#         robot.forward()


# def cross_active():
#     if leftback.is_active and rightback.is_active:
#         print("Junction stop")
#         robot.stop()
#         sys.exit()
        


    
# leftend.when_activated = leftend_active
# rightend.when_activated = rightend_active
# center.when_activated = center_active
# leftback.when_activated = cross_active
# rightback.when_activated = cross_active
def check():
    if leftback.is_active and rightback.is_active:
        print("Junction stop")
        robot.stop()
        sys.exit()

    elif center.is_active and (not leftend.is_active) and (not rightend.is_active):
        print("forward")
        robot.forward()
    elif (not leftend.is_active) and rightend.is_active:
        robot.right()
        print("right")
    elif leftend.is_active and (not rightend.is_active):
        robot.left()
        print("left")

leftend.when_activated = check
rightend.when_activated = check
center.when_activated = check
leftback.when_activated = check
rightback.when_activated = check


leftend.when_deactivated = check
rightend.when_deactivated = check
center.when_deactivated = check
leftback.when_deactivated = check
rightback.when_deactivated = check

check()

pause()



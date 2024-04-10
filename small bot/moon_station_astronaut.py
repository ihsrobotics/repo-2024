import sys
sys.path.append("/home/pi/Documents/IME_files/Small_bot_4174/include")
from bot_functions import *
from config_loader import *

# set up on left side of the horizontal line from the solar panel facing west

def go_to_station():
    k.set_servo_position(BOOM_SERVO, 630)
    k.msleep(150)

    while not on_tape(FRONT_TOPHAT, FRONT_BLACK):
        line_follow(1000, 1300, "LEFT", BOOM_TOPHAT, BOOM_BLACK)
    brake()

    while on_tape(FRONT_TOPHAT, FRONT_BLACK):
        drive(500,500)
    brake()

def turn_to_station():
    k.set_servo_position(BOOM_SERVO, 750)
    k.msleep(200)

    while not on_tape(BOOM_TOPHAT, BOOM_BLACK):
        drive(1500, -300)
    brake()

    k.set_servo_position(BOOM_SERVO, BOOM_RIGHT_POS)
    k.msleep(300)

    print(k.analog(BOOM_TOPHAT))

    while not on_tape(BOOM_TOPHAT, BOOM_BLACK):
        drive(-1100, -1500)
    brake()


def adjust():
    set_arm_pos(80)

    while on_tape(BOOM_TOPHAT, BOOM_BLACK):
        drive(500, 500)
    brake()
    print('1) ', k.analog(BOOM_TOPHAT))

    while not on_tape(BOOM_TOPHAT, BOOM_BLACK):
        drive(-100, -1000)
    brake()
    k.msleep(150)
    print('2) ', k.analog(BOOM_TOPHAT))
    while on_tape(BOOM_TOPHAT, BOOM_BLACK):
        drive(-50, -500)
    brake()
    print('3) ', k.analog(BOOM_TOPHAT))


    print('4) ', k.analog(FRONT_TOPHAT))

    while not on_tape(FRONT_TOPHAT, FRONT_BLACK):
        drive(500, 500)
    brake()
    print('5) ', k.analog(FRONT_TOPHAT))

    drive(-500, -500, 180)
    
def drop():
    brake()
    k.msleep(100)

    k.mav(ARM, -200)
    k.msleep(810)

    k.mav(ARM, 0)
    k.mav(10)

def main():
    set_arm_pos(600)

    go_to_station()
    turn_to_station()
    adjust()
    drop()

    brake()
    k.msleep(800)

    drive(-500, -500, 1500)



if __name__ == "__main__":
    k.enable_servos()
    main()

    k.disable_servos()

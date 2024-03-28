import sys
sys.path.append("/home/pi/Documents/IME_files/Small_bot_4174/include")
from bot_functions import *
from config_loader import *

# set up on left side of the horizontal line from the solar panel facing west

def go_to_middle():
    while not on_tape(BOOM_TOPHAT, BOOM_BLACK):
        line_follow(1000, 1500, "LEFT")
    brake()

def drop_stuff():
    while not on_tape(BOOM_TOPHAT, BOOM_BLACK):
        drive(1500, -1500)
    brake()
    while on_tape(BOOM_TOPHAT, BOOM_BLACK):
        drive(1500, -1500)
    brake()

    k.set_servo_position(BOOM_SERVO, 1500)
    k.msleep(100)

    while on_tape(BOOM_TOPHAT, BOOM_BLACK):
        drive(-500, -1200)
    brake()
    while not on_tape(BOOM_TOPHAT, BOOM_BLACK):
        drive(-500, -1200)
    brake()

    print(f'bruh {k.analog(FRONT_TOPHAT)}')

    while on_tape(FRONT_TOPHAT, FRONT_BLACK):
        drive(-1000, -1000)
    brake()

    drive(-300, 300, 200)

    print(f':3 {k.analog(FRONT_TOPHAT)}')


    while on_tape(FRONT_TOPHAT, FRONT_BLACK):
        drive(1000, 1000)
    brake()
    while not on_tape(FRONT_TOPHAT, FRONT_BLACK):
        drive(1000, 1000)
    brake()
    while on_tape(FRONT_TOPHAT, FRONT_BLACK):
        drive(1000, 1000)
    brake()
    print(f':P {k.analog(BOOM_TOPHAT)}')


    # while on_tape(BOOM_TOPHAT, BOOM_BLACK):
    #     drive(500, -500)
    # brake()
    # while not on_tape(BOOM_TOPHAT, BOOM_BLACK):
    #     drive(500, -500)
    # brake()

def main():
    # set_arm_pos(340)
    k.set_servo_position(BOOM_SERVO, BOOM_LEFT_POS)
    # k.set_servo_position(LEVER_SERVO, 2047)
    k.msleep(100)

    go_to_middle()
    drop_stuff()


if __name__ == "__main__":
    k.enable_servos()
    main()
    # print(k.get_servo_position(BOOM_SERVO))
    k.disable_servos()

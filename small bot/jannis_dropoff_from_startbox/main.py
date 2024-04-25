import sys
sys.path.append("/home/pi/Documents/IME_files/Small_bot_4174/include")
from bot_functions import *
from config_loader import *

def setup():
    k.set_servo_position(JANNIS_SERVO, 300)
    k.set_servo_position(BOOM_SERVO, 1740)
    k.msleep(200)
#    k.msleep(100)

def drop_limbs():

    print('bring arm in then out')
    while (k.analog(SLIDE) > 0):
        k.mav(ARM, 1000)
    stop_motor(ARM)


    # while (k.analog(SLIDE) < 4000):
    #     k.mav(ARM, -500)
    # stop_motor(ARM)


    # # for i in range(1, -1, -1):
    while (k.analog(SLIDE) < 200):
        k.mav(ARM, -500)
        print(k.analog(SLIDE))
    stop_motor(ARM)

    while (k.analog(SLIDE) > 100):
        k.mav(ARM, 1500)
    stop_motor(ARM)


def drive_to_dropoff():
    while not on_tape(FRONT_TOPHAT, FRONT_BLACK):
        drive(1500, 1500)
    brake()
    while on_tape(FRONT_TOPHAT, FRONT_BLACK):
        drive(1500, 1500)
    brake()

    drive(1500,100,1000)

    k.set_servo_position(BOOM_SERVO, BOOM_LEFT_POS)
    k.msleep(100)

    while not on_tape(BOOM_TOPHAT, BOOM_BLACK):
        drive(1500, 1500)
    brake()
    while on_tape(BOOM_TOPHAT, BOOM_BLACK):
        drive(1500, 1500)
    brake()
    while not on_tape(BOOM_TOPHAT, BOOM_BLACK):
        drive(1500, 150)
    brake()

    # while not on_tape(BOOM_TOPHAT, BOOM_BLACK):
    #     drive(1500, 1500)
    # brake()
    # while on_tape(BOOM_TOPHAT, BOOM_BLACK):
    #     drive(1500, 1500)
    # brake()
    # drive(0, 1500, 300)


def main():
    drop_limbs()
    drive_to_dropoff()
    # drive(-1500, 0, 600)
    # brake()
    # while not on_tape(FRONT_TOPHAT, FRONT_BLACK):
    #     drive(1500, 1300)
    # brake()
    # while on_tape(FRONT_TOPHAT, FRONT_BLACK):
    #     drive(1500, 1300)
    # brake()


if __name__ == "__main__":
    k.enable_servos()
    main()
    k.disable_servos()

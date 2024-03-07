from ctypes import CDLL
kipr = "/usr/local/lib/libkipr.so"
k = CDLL(kipr)

import sys

sys.path.append("/home/pi/Documents/IME_files/releaseJannis/include")

from kipr_functions import *

def setup():
    k.set_servo_position(BOOM_ARM, BOOM_ASTRONAUT_POS)
    k.set_servo_position(CLASP, CLASP_DOWN_POS)
    k.msleep(1500)

def main():
    k.set_servo_position(BOOM_ARM, BOOM_LEFT_POS)
    k.msleep(500)

    drive(500, 1500, 1300)
    brake()
    k.msleep(150)

    while (k.analog(BOOM_TOPHAT) < BOOM_BLACK):
        k.mav(LEFT_WHEEL, 1500)
        k.mav(RIGHT_WHEEL, 1500)
    brake()
    k.msleep(50)

    while (k.analog(BOOM_TOPHAT) > BOOM_BLACK):
        k.mav(LEFT_WHEEL, 1500)
        k.mav(RIGHT_WHEEL, 1500)
    brake()
    k.msleep(50)

    drive(750,750,100)

    k.set_servo_position(BOOM_ARM, 1028)

    while (k.analog(BOOM_TOPHAT) < BOOM_BLACK):
        k.mav(LEFT_WHEEL, -1500)
        k.mav(RIGHT_WHEEL, 1500)
    brake()
    k.msleep(50)

    # k.set_servo_position(BOOM_ARM, BOOM_LEFT_POS)


    

if __name__ == "__main__":
    k.enable_servos()
    setup()
    # main()
    k.disable_servos()
    k.ao()

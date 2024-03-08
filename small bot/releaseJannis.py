from ctypes import CDLL
kipr = "/usr/local/lib/libkipr.so"
k = CDLL(kipr)

import sys

sys.path.append("/home/pi/Documents/IME_files/releaseJannis/include")

from kipr_functions import *

def setup():
    k.set_servo_position(BOOM_ARM, BOOM_ASTRONAUT_POS)
    k.set_servo_position(CLASP, CLASP_DOWN_POS)
    k.msleep(500)

def part1():
    k.set_servo_position(BOOM_ARM, BOOM_LEFT_POS)
    k.msleep(10)

    drive(500, 1500, 1300)
    brake()
    k.msleep(10)


    print(':PP')
    while (k.analog(BOOM_TOPHAT) < BOOM_BLACK):
        k.mav(LEFT_WHEEL, 1500)
        k.mav(RIGHT_WHEEL, 1500)
        print(k.analog(BOOM_TOPHAT))
    brake()
    k.msleep(10)

    drive(500, 500, 200)

    print('>:3333')
    while (k.analog(BOOM_TOPHAT) > BOOM_BLACK):
        k.mav(LEFT_WHEEL, 1500)
        k.mav(RIGHT_WHEEL, 1500)
        print(k.analog(BOOM_TOPHAT))
    brake()
    k.msleep(10)

    k.set_servo_position(BOOM_ARM, 1024)
    print('arm should move to 880', k.analog(BOOM_TOPHAT))
    k.msleep(100)
    print('urhghhh', k.analog(BOOM_TOPHAT))

def part2():
    brake()
    k.msleep(500)

    while (k.analog(BOOM_TOPHAT) < BOOM_BLACK):
        k.mav(LEFT_WHEEL, -1000)
        k.mav(RIGHT_WHEEL, 1500)
    brake()
    while (k.analog(BOOM_TOPHAT) > BOOM_BLACK):
        k.mav(LEFT_WHEEL, -1000)
        k.mav(RIGHT_WHEEL, 1500)
    brake()
    
    for i in range(10):
        k.mav(LEFT_WHEEL, 1000)
        k.msleep(50)
        k.mav(RIGHT_WHEEL, 1000)
        k.msleep(50)
    brake()

if __name__ == "__main__":
    k.enable_servos()
    setup()
    # part1()
    # part2()

    k.disable_servos()
    k.ao()

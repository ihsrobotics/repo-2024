from ctypes import CDLL
kipr = "/usr/local/lib/libkipr.so"
k = CDLL(kipr)

import ihs_bindings
import sys
# print("debugger")
# import time
# time.sleep(3)
# add ../include to the import path
sys.path.append("/home/pi/Documents/IME_files/BigBotLavaTubes2024/include")

# print("debugger 2")
# time.sleep(3)

from kipr_functions import *
# from config_loader import *

def reset():
    move_servo_slowly(CLAW_PORT, CLAW_OPEN, 5)
    k.msleep(100)
    move_servo_slowly(ARM_PORT, LAVA_RESET, 10)
    k.msleep(10000)
    move_servo_slowly(CLAW_PORT, CLAW_GRAB, 5)
    k.msleep(100)
    move_servo_slowly(ARM_PORT, LARGE_LAVA_HEIGHT, 5)
    #k.disable_servos()

def main():
    drive(150, 150)
    k.msleep(385)
    drive(50, -50)
    k.msleep(700)
    ao()

if __name__ == "__main__":
    retry_connect(5)
    main()
    #reset()
    cleanup()

import sys
from ctypes import CDLL
sys.path.append("/home/pi/Documents/IME_files/lava_tube_poms/include")
from bot_functions import *
from config_loader import *
kipr = "/usr/local/lib/libkipr.so"
k = CDLL(kipr)




def main():
    while k.analog(FRONT_TOPHAT) < BLACK:
        drive(-500, -500)
    brake()
    start = k.seconds()
    while k.seconds() < start + 4825:
        line_follow(500, 700, "RIGHT", BOOM_BLACK, BOOM_TOPHAT)
    brake()
    drive(-200, 0)
    k.msleep(720)
    brake()
    

if __name__ == "__main__":
        raise_arm()
        k.enable_servos()
        k.set_servo_position(BOOM_ARM, 2047)
        k.set_servo_position(JANNIS, LOWER_JANNIS)

main()

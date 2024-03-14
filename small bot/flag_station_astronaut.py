import sys
from ctypes import CDLL
sys.path.append("/home/pi/Documents/IME_files/lava_tube_poms/include")
from bot_functions import *
from config_loader import *
kipr = "/usr/local/lib/libkipr.so"
k = CDLL(kipr)


def back_into_jannis():
    while k.analog(FRONT_TOPHAT) < BLACK:
        drive(-500, -500)
    brake()
    start = k.seconds()
    while k.seconds() < start + 4500:
        line_follow(500, 700, "RIGHT", BOOM_BLACK, BOOM_TOPHAT)
    brake()

def main():
    raise_arm()
    #Aligning with wall
    button_square_up(500)

    #Turn into area
    turn_90("LEFT")
    print("TURN FINISHED")
    brake() 
    k.msleep(300)

    #Get boom tophat off of black
    while k.analog(BOOM_TOPHAT) > BOOM_BLACK:
        drive(500, -500)
        k.msleep(10)
        print(f"BOOM: {k.analog(BOOM_TOPHAT)}/{BOOM_BLACK}")
    brake()
    start = k.seconds()
    while k.seconds() < start + 1000:
        line_follow(500, 700, "RIGHT", BOOM_BLACK, BOOM_TOPHAT)
    brake()

    #Back up onto tape
    while k.analog(FRONT_TOPHAT) < BLACK:
        drive(-500, -500)
    brake()
    k.msleep(300)

    #Line follow for duration
    start = k.seconds()
    while k.seconds() < start + 2650:
        line_follow(450, 500, "RIGHT", BOOM_BLACK, BOOM_TOPHAT)
    brake()
    
    #Turn slightly
    drive(0, -500)
    k.msleep(200)
    brake()

    #Lower arm so that the aussie barely touches the pipe
    start = k.seconds()        
    while k.analog(ARM_SLIDE) < 1000 and k.seconds() < start + 2000:
        k.mav(ARM, 1000)
        k.msleep(10)
        print("SLIDE", k.analog(ARM_SLIDE), "| TIME", k.seconds() - start)
    stop_motor(ARM)
    start = k.seconds()

    #Wiggle the aussie into the pipe
    while k.seconds() < start + 2000:
        drive(-100, 100)
        k.msleep(500)
        drive(100, -100)
        k.msleep(500)
    brake()

    #Lower arm fully into pipe
    start = k.seconds()
    while k.analog(ARM_SLIDE) < 1600 and k.seconds() < start + 2000:
        k.mav(ARM, 1000)
        k.msleep(10)
        print("SLIDE", k.analog(ARM_SLIDE), "| TIME", k.seconds() - start)
    stop_motor(ARM)

    #Back up so aussie falls in
    drive(-500, -500)
    k.msleep(1000)
    brake()

    raise_arm()
    back_into_jannis()

if __name__ == "__main__":
        k.enable_servos()
        k.set_servo_position(BOOM_ARM, 2047)
        k.set_servo_position(JANNIS, LOWER_JANNIS)

main()

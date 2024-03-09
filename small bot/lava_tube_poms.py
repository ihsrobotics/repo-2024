import sys
from ctypes import CDLL
sys.path.append("/home/pi/Documents/IME_files/lava_tube_poms/include")
from bot_functions import *
from config_loader import *
kipr = "/usr/local/lib/libkipr.so"
k = CDLL(kipr)
k.enable_servos()
k.set_servo_position(BOOM_ARM, 1940)
k.set_servo_position(JANNIS, 0)

def go_to_lava():
        k.set_servo_position(BOOM_ARM, 1940)
        #Go To Lava Tube Area
        #MAKE SURE THIS IS 2500 MS
        start = k.seconds()
        while k.seconds() < start+2500:
                line_follow(1200, 1500, "RIGHT")
        
        #Steady Line Follow Until A Button Is Clicked
        while k.analog(LEFT_BUTTON) > 1 and k.analog(RIGHT_BUTTON) > 1:
                line_follow(450, 500, "RIGHT")
                print("STEADY LINE FOLLOW", k.analog(LEFT_BUTTON), k.analog(RIGHT_BUTTON))

        #Align With The Wall
        button_square_up(500)

        #Move Slightly Backward
        drive(-500, -500)
        k.msleep(300)
        brake()

        #Adjust Angle
        while k.analog(FRONT_TOPHAT) < BLACK:
                drive(0, 300)
                k.msleep(10)

        brake()
        
        drive(0, 100)
        k.msleep(250)
        brake() 
        

def peck():
        #Lowering Arm Into Tube
        lower_arm()
        start = k.seconds()
        vibrate(2000)
        stop_motor(ARM)
        #Pecking
        for i in range(7):
                #Suck Up Poms
                k.mav(CLAW, 1500)
                k.msleep(500)
                brake()

                #Move Arm Up
                k.mav(ARM, -800)
                k.mav(CLAW, 1500)
                k.msleep(700)
                stop_motor(ARM)

                #Move Arm Down
                k.mav(ARM, 800)
                k.mav(CLAW, 1500)
                k.msleep(700)
                stop_motor(ARM)
                

def align_with_second_pipe():
        k.set_servo_position(BOOM_ARM, 1715)
        button_square_up(500)
        start = k.seconds()
        while k.seconds() < start + 2600:
                line_follow(-500, -450, "RIGHT")
        brake()
        while k.analog(BOOM_TOPHAT) < BOOM_BLACK:
                drive(100, -100)
                print("TOPHAT", k.analog(BOOM_TOPHAT))
        drive(100, -100)
        k.msleep(1000)
        while k.analog(BOOM_TOPHAT) > BOOM_BLACK:
                drive(100, -100)
                print("TOPHAT", k.analog(BOOM_TOPHAT))
        brake()

#Tasks
#1) Deploy Arm (FELIX) (DONE?)
#2) Get Astronauts (BRANDON)
#3) Deliver Astronauts (BRANDON)
#4) Drop Rack (FELIX) (DONE)
#5) Deploy The Jannis (BRANDON)
#6) Suck Up Poms (FELIX) 
#7) Deliver Poms In Point Scoring Areas (FELIX) (probably airlock)

def main():
        #POMS
        raise_arm()
        k.msleep(500)
        go_to_lava()
        peck()
        stop_motor(CLAW)
        raise_arm()
        d_pipe()
        peck()
        stop_motor(CLAW)
'''
if __name__ == "__main__":
    main()
'''

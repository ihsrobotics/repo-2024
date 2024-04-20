import sys
sys.path.append("/home/pi/Documents/IME_files/lava_tube_poms/include")
from bot_functions import *
from config_loader import *


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
        #300
        k.msleep(275)
        brake()

        #Adjust Angle
        while k.analog(FRONT_TOPHAT) < BLACK:
                drive(0, 300)
                k.msleep(10)

        brake()
        
        # drive(0, 100)
        # #250
        # k.msleep(400)
        # brake() 
        

def peck():
        k.mav(DRILL, 750)
        move_arm("GROUND")

        for i in range(7):
                #Suck Up Poms
                k.mav(DRILL, 750)
                k.msleep(500)
                

                #Move Arm Up
                k.mav(ARM, -500)
                k.mav(DRILL, 750)
                k.msleep(270)
                stop_motor(ARM)

                #Move Arm Down
                k.mav(ARM, 500)
                k.mav(DRILL, 750)
                k.msleep(270)
                stop_motor(ARM)

                k.msleep(500)

def drill_tube():
        #Drill Out Poms
        k.mav(DRILL, 1500)
        # k.msleep(12000)

        #Lowering Arm Into Tube
        move_arm("GROUND")
        k.msleep(12000)
        # start = k.seconds()

        # #Wobble Drill Into Pipe
        # while k.seconds() < start + 2000:
        #         drive(100, -100)
        #         k.msleep(500)
        #         drive(-100, 100)
        #         k.msleep(500)
        # brake()
        stop_motor(ARM)


        


def align_with_second_pipe():
        k.set_servo_position(BOOM_ARM, 1625)
        button_square_up(500)
        start = k.seconds()

        #2800
        while k.seconds() < start + 2700:
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
        move_arm("BOX")
        k.msleep(500)
        go_to_lava()
        drill_tube()
        stop_motor(DRILL)
        move_arm("BOX")
        align_with_second_pipe()
        peck()
        stop_motor(DRILL)
        move_arm("BOX")

if __name__ == "__main__":
        k.enable_servos()
        k.set_servo_position(BOOM_ARM, 1940)
        k.set_servo_position(JANNIS, 2047)
        k.set_servo_position(SWIPER, 0)

main()

#1. 3 (FAIL)
#2. 4 (PASS)
#3. 3 (FAIL)
#4. 3 (FAIL)
#5. 

import sys
sys.path.append("/home/pi/Documents/IME_files/lava_tube_poms/include")
from bot_functions import *
from config_loader import *



def main():

    #Turn until front tophat hits black
    while k.analog(FRONT_TOPHAT) < BLACK:
        drive(200, 1200)
    brake()

    #Move boom arm into box
    arm_position = k.get_servo_position(BOOM_ARM)
    while k.analog(BOOM_TOPHAT) < BLACK:
        print(f"GETTING ARM TO HIT BLACK: {k.analog(BOOM_TOPHAT)}/{BOOM_BLACK}")
        k.set_servo_position(BOOM_ARM, arm_position)
        arm_position -= 1
    while k.analog(BOOM_TOPHAT) > BLACK:
        print(f"GETTING ARM TO HIT WHITE: {k.analog(BOOM_TOPHAT)}/{BOOM_BLACK}")
        k.set_servo_position(BOOM_ARM, arm_position)
        arm_position -= 1

    #Line follow with boom arm and gradually swing it out
    while k.get_servo_position(BOOM_ARM) < 2047:
        line_follow(500, 700, "RIGHT", BOOM_BLACK, BOOM_TOPHAT)
        k.set_servo_position(BOOM_ARM, arm_position)
        arm_position += 1
        k.msleep(2)

    #Line follow for slightly longer to even out
    start = k.seconds()
    while k.seconds() < start + 3500:
        line_follow(300, 700, "RIGHT", BOOM_BLACK, BOOM_TOPHAT)
    
    

    #Back up onto tape
    while k.analog(FRONT_TOPHAT) < BLACK:
        print(f"{k.analog(FRONT_TOPHAT)} < {BLACK}")

        #OG: -550, -500
        #Left wheel is slightly faster in order to get the bot closer to the wall
        drive(-550, -500)
    brake()
    

    #Get boom off of black
    drive(500, -500)
    k.msleep(200)
    brake()

    #Line follow for duration
    start = k.seconds()
    while k.seconds() < start + 2825:
        line_follow(400, 500, "RIGHT", BOOM_BLACK, BOOM_TOPHAT)
    brake()

    #Turn slightly
    drive(0, -100)
    k.msleep(1025)
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


if __name__ == "__main__":
        k.enable_servos()
        k.set_servo_position(BOOM_ARM, 1650)
        raise_arm()
        k.set_servo_position(JANNIS, LOWER_JANNIS)
        k.set_servo_position(LEVER_SERVO, 2047)
        

main()

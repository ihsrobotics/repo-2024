import sys
sys.path.append("/home/pi/Documents/IME_files/Small_bot_4174/include")
from bot_functions import *
from config_loader import *
from time import time

def drop_limbs():
    # Bring arm in to pop it out
    while (k.analog(SLIDE) > 0):
        k.mav(ARM, 1000)
    stop_motor(ARM)

    # Lower arm to lower counterweight
    k.mav(ARM, -500)
    k.msleep(500)
    stop_motor(ARM)

def drive_to_dropoff():
    '''
    # Move out of start box
    while not on_tape(FRONT_TOPHAT, FRONT_BLACK):
        drive(1500, 1500)
    brake()
    while on_tape(FRONT_TOPHAT, FRONT_BLACK):
        drive(1500, 1500)
    brake()

    # Adjust to middle tape
    drive(1500,900,1000)
    '''
    # Line follow to middle
    k.set_servo_position(BOOM_SERVO, BOOM_RIGHT_POS)
    k.msleep(100)

    while not on_tape(FRONT_TOPHAT, FRONT_BLACK):
        line_follow(1000, 1500, "RIGHT", BOOM_TOPHAT, BOOM_BLACK)
    brake()

    k.set_servo_position(BOOM_SERVO, BOOM_LEFT_POS)
    k.msleep(100)

    # Rough 90 turn to face towards dropoff
    drive(1500, -1500, 750)
    brake()

    # Move closer to dropoff
    while not on_tape(FRONT_TOPHAT, FRONT_BLACK):
        drive(800, 1500)
    brake()
    while on_tape(FRONT_TOPHAT, FRONT_BLACK):
        drive(800, 1500)
    brake()
    drive(800, 1500, 400) # Make sure we're off the line
    brake()
    while not on_tape(FRONT_TOPHAT, FRONT_BLACK):
        drive(800, 1500)
    brake()

    while not on_tape(BOOM_TOPHAT, BOOM_BLACK):
        line_follow(1000, 1500, "RIGHT", FRONT_TOPHAT, FRONT_BLACK)
    brake()

    while not on_tape(BOOM_TOPHAT, BOOM_BLACK):
        drive(1500, 1500)
    brake()
    while on_tape(BOOM_TOPHAT, BOOM_BLACK):
        drive(1500, 1500)
    brake()

def drop_jannis():
    # Line follow to straighten out
    start = time()
    while time() - start < 3.1:
        line_follow(500, 1500, "RIGHT", BOOM_TOPHAT, BOOM_BLACK)
    brake()

    # Move to drop off spot
    # drive(-500, -500, 1500) # INCREASE NOW
    # brake()

    # k.cmpc(LEFT_WHEEL)
    # k.cmpc(RIGHT_WHEEL)
    # bruh = -4
    # while k.gmpc(LEFT_WHEEL) > bruh and k.gmpc(RIGHT_WHEEL) > bruh:
    #     if (k.gmpc(LEFT_WHEEL) > bruh): k.mav(LEFT_WHEEL, -300)
    #     else: k.mav(LEFT_WHEEL, 0)

    #     if (k.gmpc(RIGHT_WHEEL) > bruh): k.mav(RIGHT_WHEEL, -300)
    #     else: k.mav(RIGHT_WHEEL, 0)
    # brake()


    # # Push Jannis into wall
    # drive(-500, 500, 300)
    # brake()

    # drive(-500, 0, 230)
    # brake()
    '''
    # Unclasp Jannis
    k.enable_servo(JANNIS_SERVO)
    for i in range(k.get_servo_position(JANNIS_SERVO), 2000):
        k.set_servo_position(JANNIS_SERVO, i)
        k.msleep(1)

    # Turn to get counterweight out the way (temporary)
    drive(300, 50, 1000)
    brake()
    '''
    

# Just used for testing
def tube_drop():
    print('Running... Waiting now...')
    while k.digital(RIGHT_BUTTON) != 1: 
        k.msleep(500)
    print('Done waiting :PP')
    k.ao()
    k.enable_servo(0)
    k.set_servo_position(0, 2047)
    k.msleep(100)
    k.disable_servo(0)

    is_open = False

    while True:
        if k.digital(LEFT_BUTTON) == 1:
            print('Pressed! >_<')
            k.enable_servo(0)
            if is_open: 
                k.set_servo_position(0, 2047)
            else:
                k.set_servo_position(0, 0)
            k.disable_servo(0)
            is_open = not is_open
            k.msleep(3000)
        k.msleep(100)

def main():
    # drop_limbs()
    drive_to_dropoff()
    drop_jannis()

if __name__ == "__main__":
    k.enable_servos()
    main()
    k.disable_servos()
    # tube_drop()

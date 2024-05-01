import sys
sys.path.append("/home/pi/Documents/IME_files/start_seq/include")
from bot_functions import *
from config_loader import *
from time import time

def lower_arm_to_pickup():
    while k.analog(SLIDE) > 0:
        k.mav(ARM, -1500)
    stop_motor(ARM)

    while k.analog(SLIDE) < 5:
        k.mav(ARM, 1500)
    stop_motor(ARM)

def drive_to_astronaut_pickup():
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

    # Rough 90 turn to face towards pickup
    drive(1500, -1500, 850)
    brake()

    k.set_servo_position(BOOM_SERVO, 1720)
    k.msleep(100)

    lower_arm_to_pickup()

    while not on_tape(BOOM_TOPHAT, BOOM_BLACK):
        drive(500, 1000)
    brake()

    start = time()
    while time() - start < 1:
        line_follow(500, 1000, "RIGHT", BOOM_TOPHAT, BOOM_BLACK)
    brake()

    start = time()
    while time() - start < 2.5: # 7 secs without the fast line follow
        line_follow(100, 200, "RIGHT", BOOM_TOPHAT, BOOM_BLACK)
    brake()

    # drive(1000, 1000, 100)
    # brake()

def drive_to_jannis_dropoff():
    k.set_servo_position(BOOM_SERVO, BOOM_LEFT_POS)
    k.msleep(100)

    while not on_tape(FRONT_TOPHAT, FRONT_BLACK):
        drive(-500, 1500)
    brake()

    while not on_tape(BOOM_TOPHAT, BOOM_BLACK):
        drive(1500, 700)
    brake()
    while on_tape(BOOM_TOPHAT, BOOM_BLACK):
        drive(1500, 700)
    brake()

    while not on_tape(BOOM_TOPHAT, BOOM_BLACK):
        drive(400, 1500)
    brake()

    start = time()
    while time() - start < 2:
        line_follow(600, 1500, "RIGHT", BOOM_TOPHAT, BOOM_BLACK)
    brake()
    start = time()
    while time() - start < 2:
        line_follow(400, 800, "RIGHT", BOOM_TOPHAT, BOOM_BLACK)
    brake()

    # Move to drop off spot
    while k.digital(SWITCH) == 0:
        drive(-1000, -950)
    brake()

    # Move forward
    drive(500, 500, 1500)
    brake()

    # # Push Jannis into wall
    # drive(-500, 500, 300)
    # brake()

    # drive(-500, 0, 230)
    # brake()

def main():
    while k.analog(SLIDE) != 0:
        k.mav(ARM, -1500)
    stop_motor(ARM)

    drive_to_astronaut_pickup()

    while k.analog(SLIDE) != 0:
        k.mav(ARM, -1500)
    stop_motor(ARM)

    drive_to_jannis_dropoff()

if __name__ == "__main__":
    timer = time()
    k.enable_servos()
    main()
    k.disable_servos()
    print("Runtime in secs:", time() - timer)

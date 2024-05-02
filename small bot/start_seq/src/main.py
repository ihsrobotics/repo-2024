import sys
sys.path.append("/home/pi/Documents/IME_files/start_seq/include")
from bot_functions import *
from config_loader import *
from time import time

def lower_arm_to_pickup():
    # while k.analog(SLIDE) > ARM_UP_POS:
    #     k.mav(ARM, -1500)
    # stop_motor(ARM)

    while k.analog(SLIDE) < ARM_DOWN_POS:
        k.mav(ARM, 1500)
    stop_motor(ARM)

def drop_limbs():
    # Bring arm in to pop it out
    while (k.analog(SLIDE) > ARM_UP_POS):
        k.mav(ARM, -1500)
    stop_motor(ARM)

    # Lower arm to lower counterweight
    k.mav(ARM, -500)
    k.msleep(500)
    stop_motor(ARM)

def leave_start_box():
    # Move out of start box
    while not on_tape(FRONT_TOPHAT, FRONT_BLACK):
        drive(1500, 1500)
    brake()
    while on_tape(FRONT_TOPHAT, FRONT_BLACK):
        drive(1500, 1500)
    brake()

    # Raise ARM to up position
    while k.analog(SLIDE) > ARM_UP_POS:
        k.mav(ARM, -1500)
    stop_motor(ARM)

    # Adjust to middle tape
    drive(1500,900,1000)

def drive_to_astronaut_pickup(): 
    # Line follow to middle
    k.set_servo_position(BOOM_SERVO, BOOM_RIGHT_POS)
    k.msleep(100)

    while not on_tape(FRONT_TOPHAT, FRONT_BLACK):
        line_follow(1000, 1500, "RIGHT", BOOM_TOPHAT, BOOM_BLACK)
    brake()

    # Set BOOM to the right position for the pickup
    k.set_servo_position(BOOM_SERVO, BOOM_ASTRO_PICKUP_POS)
    k.msleep(100)

    # Rough 90 turn to face toward pickup spot
    drive(1500, -1500, 850)
    brake()

    lower_arm_to_pickup()

    # Adjust to tape before line following
    while not on_tape(BOOM_TOPHAT, BOOM_BLACK):
        drive(500, 1000)
    brake()

    # Fast line follow to astronauts
    start = time()
    while time() - start < 1.2:
        line_follow(500, 1000, "RIGHT", BOOM_TOPHAT, BOOM_BLACK)
    brake()

    # Slow line follow to astronauts
    start = time()
    while time() - start < 2.9: # 7 secs without the fast line follow
        line_follow(100, 200, "RIGHT", BOOM_TOPHAT, BOOM_BLACK)
    brake()

def pick_up_astronauts():
    # Raise ARM to up position
    while k.analog(SLIDE) > ARM_UP_POS:
        k.mav(ARM, -1500)
    stop_motor(ARM)

def drive_to_jannis_dropoff():
    # Set BOOM to Jannis-dropoff line follow position
    k.set_servo_position(BOOM_SERVO, BOOM_LEFT_POS)
    k.msleep(100)

    # Turn to start line follow
    while not on_tape(FRONT_TOPHAT, FRONT_BLACK):
        drive(-600, 1500)
    brake()

    # Drive forward until BOOM is ready to line follow along the tape
    while not on_tape(BOOM_TOPHAT, BOOM_BLACK):
        drive(1500, 1000)
    brake()
    while on_tape(BOOM_TOPHAT, BOOM_BLACK):
        drive(1500, 1000)
    brake()

    # Fast line follow to straighten out
    start = time()
    while time() - start < 2:
        line_follow(600, 1500, "RIGHT", BOOM_TOPHAT, BOOM_BLACK)
    brake()
    
    # Slow line follow to straighten out
    start = time()
    while time() - start < 2:
        line_follow(400, 800, "RIGHT", BOOM_TOPHAT, BOOM_BLACK)
    brake()

    # Drive backwards to dropoff spot
    while k.digital(SWITCH) == 0:
        drive(-1500, -1300)
    brake()

    # Drive forward to adjust Jannis
    k.cmpc(LEFT_WHEEL)
    k.cmpc(RIGHT_WHEEL)
    while k.gmpc(LEFT_WHEEL) < 600 or k.gmpc(RIGHT_WHEEL) < 700: # idk why these vals r diff but it works ig
        drive(500, 500)
    brake()
    k.disable_servos()

    # Push Jannis into wall
    drive(-500, 500, 300)
    brake()

def drop_jannis():
    k.enable_servo(JANNIS_SERVO)

    # Unclasp Jannis
    for i in range(k.get_servo_position(JANNIS_SERVO), 2000):
        k.set_servo_position(JANNIS_SERVO, i)
        k.msleep(1)
        
    k.disable_servo(JANNIS_SERVO)

    # Turn to get counterweight out the way (temporary)
    drive(300, 100, 1000)
    brake()

def main():
    # Temporary - the ARM will already be up after leave_start_box()
    while k.analog(SLIDE) > ARM_UP_POS:
        k.mav(ARM, -1500)
    stop_motor(ARM)


    # drop_limbs()
    # leave_start_box()
    drive_to_astronaut_pickup()
    pick_up_astronauts()
    
    drive_to_jannis_dropoff()
    drop_jannis()

if __name__ == "__main__":
    timer = time()
    k.enable_servos()
    main()
    k.disable_servos()
    print("Runtime in seconds:", time() - timer)

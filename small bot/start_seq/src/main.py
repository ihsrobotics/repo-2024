import sys
sys.path.append("/home/pi/Documents/IME_files/start_seq/include")
from bot_functions import *
from config_loader import *
from time import time

def drop_limbs():
    # Bring arm in to pop it out
    raise_arm_up()

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

    # # Raise ARM to up position
    # raise_arm_up() might not need this...

    # Adjust to middle tape
    drive(1500, 900, 1000)

def drive_to_astronaut_pickup(): 
    # Line follow to middle line
    k.set_servo_position(BOOM_SERVO, BOOM_RIGHT_POS)
    k.msleep(100)

    while not on_tape(FRONT_TOPHAT, FRONT_BLACK):
        line_follow(1000, 1500, "RIGHT", BOOM_TOPHAT, BOOM_BLACK)
    brake()

    # Set BOOM to the correct position for the pickup
    k.set_servo_position(BOOM_SERVO, BOOM_ASTRO_PICKUP_POS)
    k.msleep(100)

    # Turn to face toward pickup spot
    while not on_tape(BOOM_TOPHAT, BOOM_BLACK):
        drive(1500, -1500)
    brake()
    while on_tape(BOOM_TOPHAT, BOOM_BLACK):
        drive(1500, -1500)
    brake()

    lower_arm_to_pickup()

    # Fast line follow to astronauts
    start = time()
    while time() - start < 1.45:
        line_follow(500, 1000, "RIGHT", BOOM_TOPHAT, BOOM_BLACK)
    brake()

    # Slow line follow to astronauts
    start = time()
    while time() - start < 2.8: # 7 secs without the fast line follow
        line_follow(100, 200, "RIGHT", BOOM_TOPHAT, BOOM_BLACK)
    brake()

def pick_up_astronauts():
    # Raise ARM to up position
    raise_arm_up()

def drive_to_first_dropoff():
    # Prepare to drive forward to dropoff
    k.set_servo_position(BOOM_SERVO, BOOM_LEFT_POS)
    k.msleep(100)

    # Turn toward dropoff
    while not on_tape(FRONT_TOPHAT, FRONT_BLACK):
        drive(-600, 1500)
    brake()

    # Drive forward to dropoff
    while not on_tape(BOOM_TOPHAT, BOOM_BLACK):
        drive(1500, 1000)
    brake()
    while on_tape(BOOM_TOPHAT, BOOM_BLACK):
        drive(1500, 1000)
    brake()

    # Turn to dropoff hole
    k.set_servo_position(BOOM_SERVO, 1460)
    k.msleep(300) # longer wait to get accurate values

    while not on_tape(BOOM_TOPHAT, BOOM_BLACK):
        drive(0, 1000)
    brake()

    # Drive closer to dropoff hole
    clear_ticks()
    while k.gmpc(LEFT_WHEEL) < 120 or k.gmpc(RIGHT_WHEEL) < 120:
        drive(500, 500)
    brake()

def drop_first():
    # Lower arm to hover over dropoff hole
    while k.analog(SLIDE) < 2350: # ARM_FIRST_HOVER_POS
        k.mav(ARM, 700)
    stop_motor(ARM)

    # Wiggle to get astronaut in hole
    for i in range(2):
        drive(200, -200, 200)
        brake()
        drive(-200, 200, 200)
        brake()
    brake()

    # Lower arm & drive backwards to release astronaut
    k.mav(ARM, 900)
    k.msleep(100)
    stop_motor(ARM)

    drive(-1000, -1000, 200)
    brake()

    # Set BOOM to Jannis dropoff line follow position in advance
    k.set_servo_position(BOOM_SERVO, BOOM_LEFT_POS)
    k.msleep(100)

    # Raise ARM to up position
    raise_arm_up() # maybe not necessary to go all the way up. think abt it

def drive_to_jannis_dropoff():
    # Turn to get BOOM tophat on the tape
    while not on_tape(BOOM_TOPHAT, BOOM_BLACK):
        drive(1500, -1500)
    brake()
    while on_tape(BOOM_TOPHAT, BOOM_BLACK):
        drive(1500, -1500)
    brake()

    # Fast line follow to straighten out
    start = time()
    while time() - start < 2:
        line_follow(600, 1500, "RIGHT", BOOM_TOPHAT, BOOM_BLACK)
    brake()
    
    # Slow line follow to straighten out
    start = time()
    while time() - start < 1.0:
        line_follow(400, 800, "RIGHT", BOOM_TOPHAT, BOOM_BLACK)
    brake()

    # Drive backwards to dropoff spot
    while k.digital(SWITCH) == 0:
        drive(-1500, -1250)
    brake()

    # Drive forward to get Jannis in dropoff spot
    clear_ticks()
    while k.gmpc(LEFT_WHEEL) < 770 or k.gmpc(RIGHT_WHEEL) < 770: 
        drive(500, 500)
    brake()

def drop_jannis():
    # Unclasp Jannis
    for i in range(k.get_servo_position(JANNIS_SERVO), 2047+1):
        k.set_servo_position(JANNIS_SERVO, i)
        k.msleep(1)

    # Push Jannis into wall
    drive(-500, 500, 300)
    brake()

    # Turn to get counterweight out the way (temporary)
    drive(300, 100, 1000)
    brake()

def main():

    # drop_limbs()
    # leave_start_box()

    # Temporary - the ARM will already be up after leave_start_box()
    raise_arm_up()

    drive_to_astronaut_pickup()
    pick_up_astronauts()
    drive_to_first_dropoff()
    drop_first()
    drive_to_jannis_dropoff()
    drop_jannis()

if __name__ == "__main__":
    timer = time()
    k.enable_servos()
    main()
    k.disable_servos()
    print("Runtime in seconds:", time() - timer)

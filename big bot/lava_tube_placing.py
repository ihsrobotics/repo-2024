from ctypes import CDLL
kipr = "/usr/local/lib/libkipr.so"
k = CDLL(kipr)

import ihs_bindings
import sys
import time
# print("debugger")
# import time
# time.sleep(3)
# add ../include to the import path
sys.path.append("/home/pi/Documents/IME_files/BigBotLavaTubes2024/include")

# print("debugger 2")
# time.sleep(3)

from kipr_functions import *
# from config_loader import *

STRAIGHT = "STRAIGHT"
TURN = "TURN"

def shake_straight(speed):
    amount = 0
    while amount < 5:
        drive(-speed, -speed)
        k.msleep(250)
        drive(speed, speed)
        k.msleep(250)
        amount += 1
    drive(0, 0)
def shake_turn(speed):
    amount = 0
    while amount < 5:
        drive(speed, -speed)
        k.msleep(100)
        drive(-speed, speed)
        k.msleep(200)
        drive(speed, -speed)
        k.msleep(100)
        amount += 1
    drive(0, 0)
def shake(direction):
    amount = 0
    print ("Shaking")
    if direction == STRAIGHT:
        while amount < 5:
            drive(-75, -75)
            k.msleep(250)
            drive(75, 75)
            k.msleep(250)
            amount += 1
    if direction == TURN:
        while amount < 5:
            drive(50, -50)
            k.msleep(100)
            drive(-50, 50)
            k.msleep(200)
            drive(50, -50)
            k.msleep(100)
            amount += 1
    drive(0, 0)

def claw_shake():
    amount = 0
    while amount < 5:
        servo(CLAW_PORT, LAVA_OPEN)
        k.msleep(10)
        servo(CLAW_PORT, CLAW_GRAB)
        k.msleep(10)
        amount += 1
    servo(CLAW_PORT, LAVA_OPEN)
    k.msleep(50)

def main():
    #move side servo to 1297, black rod should be alined with far side of black tape

    start_time = time.time()
    #large lava tube
    servo(ARM_PORT, LARGE_LAVA_HEIGHT)
    move_servo_slowly(CLAW_PORT, CLAW_GRAB, 5)
    move_servo_slowly(ARM_PORT, LARGE_LAVA_HEIGHT, 5)
    
    move_servo_slowly(SIDE_SERVO_PORT, 528, 5) #orginally 620
    drive(30, -30)
    while k.analog(SIDE_TOPHAT_PORT) < SENSOR_BLACK:
        pass
    drive(0, 0)

    move_servo_slowly(CLAW_PORT, LAVA_OPEN, 5)

    k.msleep(1000) #test pause

    shake_straight(100) # first poodle has more friction from extra top poodle, needs more speed for effective shake
    shake_turn(50)

    move_servo_slowly(ARM_PORT, 213, 5)
    move_servo_slowly(CLAW_PORT, CLAW_GRAB, 1)
    move_servo_slowly(ARM_PORT, LARGE_LAVA_HEIGHT, 1)

    #medium lava tube
    move_servo_slowly(SIDE_SERVO_PORT, 760, 5) #orginally 769    
    ihs_bindings.encoder_turn_degrees_v2(100, -15)
    drive(20, -20)
    move_servo_slowly(ARM_PORT, MEDIUM_LAVA_HEIGHT, 5)
    while k.analog(SIDE_TOPHAT_PORT) < SENSOR_BLACK:
        pass
    drive(0, 0)
    drive(70, 70)
    k.msleep(250)
    drive(0, 0)
    move_servo_slowly(ARM_PORT, LARGE_LAVA_HEIGHT, 5) # move to clear the other pipe and allow claw to open fully
    move_servo_slowly(CLAW_PORT, LAVA_OPEN, 5)
    k.msleep(500) # give time for poodle to fall out
    shake_straight(75)
    shake_turn(50)
    print(time.time() - start_time)
"""
    #moves away from tubes
    servo(ARM_PORT, LARGE_LAVA_HEIGHT)
    drive(100, 100)
    k.msleep(500)
    move_servo_slowly(CLAW_PORT, CLAW_OPEN, 5)
"""

if __name__ == "__main__":
    k.enable_servos()
    retry_connect(5)
    main()
    cleanup()

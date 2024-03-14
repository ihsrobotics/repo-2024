from ctypes import CDLL
kipr = "/usr/local/lib/libkipr.so"
k = CDLL(kipr)

import ihs_bindings
import sys
# print("debugger")
# import time
# time.sleep(3)
# add ../include to the import path
sys.path.append("/home/pi/Documents/IME_files/BigBotNoodlePlacement2024/include")

# print("debugger 2")
# time.sleep(3)

from kipr_functions import *
# from config_loader import *


def first_pipe():
    # put on hold while the boom arm is being developed
    drive_to_line(-150, -150, left_side, right_side)
    #move_servo_slowly(ARM_PORT, ARM_STRAIGHT_UP, 10)
    drive(-150, -150)
    k.msleep(1600)
    #this portion would be encoder_turn_degrees_v2 if ihsboost worked!!!
    drive(-150, 150)
    k.msleep(1190)
    drive(-150, -150)
    k.msleep(900)
    drive(0, 0)
    move_servo_slowly(ARM_PORT, ARM_DOWN, 5)


#def medium_pipe():
    # insert code
    # note: move back abt 3000 ms

def center_line_to_large():
    # # square up with line running through center and raise arm
    drive_to_line(150, 150, left_side, right_side)
    # move off of center line
    drive(150, 150)
    k.msleep(1500)
    # line follow on top right horizontal tape, stop when reaching the top right vertical tape
    while (left_side() > BLACK):
        if (left_front() < BLACK):
            k.create_drive_direct(150, 250)
        if(left_front() > BLACK):
            k.create_drive_direct(250, 150)
    # once at the top right vertical tape, drive slightly forward to somewhat center the bot
    drive(150, 150)
    k.msleep(500)
    # rotate the bot to have the arm lower down outside of the black tape
    drive(150, -150)
    k.msleep(700)
    ao()
    move_servo_slowly(ARM_PORT, 0, 20)
    # wait to ensure that the arm is all the way down
    k.msleep(1000)
    # rotate the bot until the tophat port at the end of the arm is aligned with the trv tape
    while (k.analog(ARM_TOPHAT_PORT) < SENSOR_BLACK):
        drive(25, -25)
    drive(-50, 50)
    k.msleep(50)
    drive(0, 0)
    move_servo_slowly(ARM_PORT, ARM_STRAIGHT_UP, 10)
    k.msleep(500)
    while (left_front() > BLACK):
        drive(-150, -150)
    ihs_bindings.encoder_turn_degrees_v2(100, 2)
    drive(-150, -150)
    msleep(300)
    drive(0, 0)


def large_pipe():
    move_servo(SIDE_SERVO_PORT, SIDE_LEFT)
    move_servo_slowly(ARM_PORT, 1150, 10) #orginally 792, also 1050
    turn_180(True)
    drive(-75, -75)
    k.msleep(150)
    ao()
    #move_servo_slowly(ARM_PORT, 875, 5) 875 should be 792
    #move_servo(ARM_PORT, 875)
    #k.msleep(200)
    #ao()
	#move_servo_slowly(ARM_PORT, 790, 5)
    #ihs_bindings.encoder_turn_degrees_v2(15, -1)
    drive(9, 9)
    move_servo_slowly(ARM_PORT, 792, 10)
    drive(0, 0)
    #move_servo(CLAW_PORT, CLAW_OPEN)
    k.msleep(500)
    for i in range(5):
        drive(-100, 100)
        k.msleep(100)
        drive(100, -100)
        k.msleep(100)
    """drive(150, 150)
    k.msleep(300)"""
    ao()

#def fourth_pipe():
    # insert code

#def fifth_pipe():
    # insert code



if __name__ == "__main__":
    print("hello world")
    #print(configs)
    retry_connect(5)
    k.enable_servos()
    start = k.seconds()
    large_pipe()
    print(k.seconds() - start)
    cleanup()

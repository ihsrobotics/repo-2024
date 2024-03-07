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

"""
def noodle_grab():
	retry_connect(5)
	k.enable_servos()
	#drive forward towards the rack
	drive(150, 150)
	k.msleep(321) #orig 271 for the center right of the rack when facing it
	
	#all this is for placing the noodle on the center right of the rack
	#ihs_bindings.encoder_turn_degrees_v2(100, -160)
	#move_servo_slowly(ARM_PORT, ARM_STRAIGHT, 3)
	
	#rotate so claw (that's holding a noodle) is facing a rack prong
	ihs_bindings.encoder_turn_degrees_v2(100, -147.5)
	#lift arm down so that noodle is halfway penetrated by prong
	move_servo_slowly(ARM_PORT, ARM_ON_RACK, 2)
	#let go of noodle
	k.msleep(500)
	k.enable_servos()
	k.set_servo_position(CLAW_PORT, CLAW_OPEN)
	k.enable_servos()
	k.msleep(3000)
	#note: may not need this turn after the claw redesign
	#turn slghtly so that noodle is not stuck on black prong on claw
	ihs_bindings.encoder_turn_degrees_v2(100, -3)
	k.msleep(250)
	move_servo_slowly(ARM_PORT, ARM_STRAIGHT_UP, 3)
	#ihs_bindings.encoder_turn_degrees(100, 147)
	drive(100, -100)
	k.msleep(250)
	move_servo_slowly(ARM_PORT, ARM_DOWN, 10)
	k.msleep(500)
	while (k.analog(ARM_TOPHAT_PORT) < SENSOR_BLACK):
		drive(50, -50)
		print(k.analog(ARM_TOPHAT_PORT))
	drive(-100, -100)
	k.msleep(321)
	k.disable_servos()
"""

"""
def main():
	success = retry_connect(5) ## connects to but, tries 5 times
	if not success:
		print("Failed to connect!!!")
		return -1
	print_battery_info()
	start_time = k.seconds()

	#line up arm with free-standing structure left most rods
	move_servo_slowly(ARM_PORT, ARM_STRAIGHT_UP, 10) #orig step: 5
	move_servo(CLAW_PORT, CLAW_OPEN)
	ihs_bindings.encoder_turn_degrees_v2(100, -40)
	drive_to_line(200, 200, left_side, right_side) #orig speed: 100, 100
	ihs_bindings.encoder_turn_degrees_v2(200, -2) #orig speed: 100, -2, deg originally -3 but DO NOT CHANGE since -2 is good
	k.msleep(100)
	drive(-100, -100) #orig speed: -50, -50
	k.msleep(350) #orig time: 500

	k.create_stop()

	#grab free standing structure
	move_servo_slowly(ARM_PORT, ARM_STRAIGHT, 3) ## lowers hand to grab Structure
	k.msleep(100) #orig time: 1000

	move_servo(CLAW_PORT, CLAW_CLOSED) ## closes claw
	k.enable_servos()
	move_servo_slowly(ARM_PORT, ARM_GRAB)
	k.msleep(100) #orig time: 500
	drive(300, 300) #orig speed: 150, 150
	k.msleep(1000) #orig time: 2000

	
	#turn out of box
	#ihs_bindings.encoder_turn_degrees_v2(100, -20)
	#drive(100, 100)
	#k.msleep(500)
	

	#drive foward to middle of white space
	drive(300, 300) #orig speed: 150, 150
	k.msleep(600) #orig time: 1200
	ihs_bindings.encoder_turn_degrees_v2(100, 90) #orig speed: 50, 90 deg clockwise

	#go to middle line
	#ihs_bindings.encoder_turn_degrees_v2(100, -5)
	#while (k.analog(BACK_TOPHAT) < 1000):
		#drive(-150, -150)
	drive_to_line(-150, -150, left_side, right_side) #orig speed: -150, -150
	#drive(100, 100)
	#drive(-150, -150)
	#k.msleep(300)

	#move forward an arbitrary amount to center the roomba on the line (I LOVR HARDCODE>>>>)
	drive(150, 150) #orig speed: 150, 150
	k.msleep(400) #orig time: 400
	drive(0, 0)

	#turn 90 to place structure structure 
	ihs_bindings.encoder_turn_degrees_v2(100, 97) #orig speed: 100, 97 deg clockwise

	#release structure
	move_servo(CLAW_PORT, CLAW_OPEN)
	k.enable_servos()
	move_servo_slowly(ARM_PORT, ARM_STRAIGHT_UP, 10) #orig step: 5
	#drive_to_line(-250, -200, k.get_create_lcliff_amt, k.get_create_rcliff_amt)

	#center on black line
	#while (left_side() and right_side() and left_front() and right_front()) > BLACK and BACK_TOPHAT < BLACK:
	#	drive(100, -100)
	ihs_bindings.encoder_turn_degrees_v2(100, 165) #orig speed: 100, 165 deg clockwise
	drive(-150, -150) #orig speed: -150, -150
	k.msleep(271) #orig time: 271

	#INSERT NOODLE GRABBING CODE HERE:
	#noodle garb
    
	#print the time elapsed since the start of the program
	print(k.seconds() - start_time)
	k.create_disconnect()
	k.disable_servos()
    """

def reset():
    move_servo_slowly(ARM_PORT, ARM_STRAIGHT_UP, 10)
    move_servo_slowly(CLAW_PORT, CLAW_GRAB, 5)


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


#def second_pipe():
    # insert code
    # note: move back abt 3000 ms

def third_pipe():
    # square up with line running through center and raise arm
    drive_to_line(150, 150, left_side, right_side)
    #move_servo_slowly(ARM_PORT, ARM_STRAIGHT_UP, 10)
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
    servo(ARM_PORT, 0, 10)
    # wait to ensure that the arm is all the way down
    k.msleep(500)
    # rotate the bot until the tophat port at the end of the arm is aligned with the trv tape
    while (k.analog(ARM_TOPHAT_PORT) < SENSOR_BLACK):
        drive(25, -25)
    drive(-50, 50)
    k.msleep(50)
    drive(0, 0)
    servo(ARM_PORT, ARM_STRAIGHT_UP, 10)
    k.msleep(500)
    while (left_front() > BLACK):
        drive(-150, -150)
    ihs_bindings.encoder_turn_degrees_v2(100, 2)
    drive(-150, -150)
    k.msleep(300)
    drive(0, 0)
    servo(ARM_PORT, 875, 5)
    k.msleep(500)
    move_servo(CLAW_PORT, CLAW_OPEN)
    


#def fourth_pipe():
    # insert code

#def fifth_pipe():
    # insert code



# #main
# retry_connect(5)
# #reset()
# #third_pipe()

# #THIS IS FOR TESTING TO SEE IF THE BOT ACTUALLY ACCURATELY ROTATES 180 !!! HELP
# """drive_to_line(150, 150, left_side, right_side)
# while k.analog(SIDE_TOPHAT_PORT) < SENSOR_BLACK:
#         drive(150, 150)
# drive(-150, -150)
# k.msleep(1050)
# drive(0, 0)
# k.msleep(2000)"""

# turn_180(True)
# k.msleep(3000)
# drive(-150, -150)
# k.msleep(500)
# turn_180()

# """drive(-150, -150)
# k.msleep(700)
# turn_180()"""
# """turn_180()
# drive(-150, -150)
# k.msleep(1050)
# drive(0, 0)"""

# cleanup()

if __name__ == "__main__":
	print("hello world")
	#print(configs)
	retry_connect(5)
	k.enable_servos()
	start = k.seconds()
	third_pipe()

	print(k.seconds() - start)
	cleanup()

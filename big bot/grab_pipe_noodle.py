from ctypes import CDLL
kipr = "/usr/local/lib/libkipr.so"
k = CDLL(kipr)

import ihs_bindings
import sys
import math
import time

sys.path.append("/home/pi/Documents/IME_files/grabNoodle/include")
from sensorshortcuts import *
from constants import *
#sensor test
##while True:
##	print (left_side(), "left side")
##	print (" ")
#	print (left_front(), "left front")
#	print (" ")
#	print (right_side(), "right side")
#	print (" ")
#	print (right_front(), "right front")
#	print (" ")

def retry_connect(n):
	for i in range(n):
		print("Attempt to connect")
		success = k.create_connect_once()
		if success:
			print("Connected ^w^")
			return True
	print("Failed to connect!!!")
	print("Check if roomba is on")
	print("Also, check the cable connecting the controller to the roomba.")
	sys.exit(-1)
def cleanup():
	k.create_disconnect()
	k.disable_servos()
# higher delay value = slower servo move
# the servo is disabled after calling the function
# to protect microservoes
def move_servo_slowly(port, end_position, delay=0):
	k.enable_servo(port)
	position = k.get_servo_position(port)
	if end_position == position:
	    return
	elif delay == 0:
	    k.set_servo_position(port, end_position)
	    msleep(100)
	    return
	while k.get_servo_position(port) < end_position and k.get_servo_position(port)+5 < 2048:
		position = k.get_servo_position(port)+5
		k.set_servo_position(port, position)
		k.msleep(delay)
	while k.get_servo_position(port) > end_position and k.get_servo_position(port)-5 > 0:
		position = k.get_servo_position(port)-5
		k.set_servo_position(port, position)
		k.msleep(delay)
	k.set_servo_position(port, end_position); k.msleep(100)

# instantly moves servo
# enables servo before moving servo
# disables servo after to protect microservoes
def move_servo(port, end_position):
	k.enable_servo(port)
	k.set_servo_position(port, end_position)
	k.msleep(100)
	k.disable_servo(port)

# chews the claw by opening and closing it
# also vibrates arm up and down
# helps grab the noodle better
def chew_claw(count):
	move_servo(CLAW_PORT,CLAW_OPEN)
	arm_position = k.get_servo_position(ARM_PORT)
	deviance = count*3
	drive(-11,-11)

	for i in range(count, 0, -1):
        #button condition
		if i == count - 2:
			drive(0, 0)
		if i % 2 == 0:
			move_servo(ARM_PORT, math.floor(arm_position + deviance))
		else:
			move_servo(ARM_PORT, math.floor(arm_position - deviance))
		deviance -= 3
		move_servo(CLAW_PORT, int(CLAW_CLOSED + (CLAW_OPEN - CLAW_CLOSED) * i/count))
		k.msleep(1)
		move_servo(CLAW_PORT,CLAW_CLOSED)
		k.msleep(1)
	move_servo(ARM_PORT, arm_position)
#square up
def drive_to_line(left_speed, right_speed, left_sensor=left_front, right_sensor=right_front):
	print (left_sensor(), right_sensor())
	while (left_sensor() > BLACK and right_sensor() > BLACK):
		drive(left_speed, right_speed)
	while (left_sensor() > BLACK):
		drive(left_speed, 0)
	while (right_sensor() > BLACK):
		drive(0, right_speed)
	while (left_sensor() > BLACK):
		drive(left_speed, 0)
	drive(0,0)
	return
#gyro_turn_degrees_v2(100,180)
#square up ON WHITE!!!!
def drive_to_line_white(left_speed, right_speed, left_sensor, right_sensor):
	print (left_sensor(), right_sensor())
	while (left_sensor() < BLACK and right_sensor() < BLACK):
		drive(left_speed, right_speed)
	while (left_sensor() < BLACK):
		drive(left_speed, 0)
	while(right_sensor() < BLACK):
		drive(0, right_speed)
	return

def line_follow(port, seconds):
	end_time = seconds*1000
	start = k.seconds()
	while (k.seconds() - start < end_time):
		if (port() < BLACK):
			k.create_drive_direct(250, 150)
		if(port() > BLACK):
			k.create_drive_direct(150, 250)
def test_drag():
	success = retry_connect(5)
	if not success:
		print("Failed to connect!!!")
		return -1
	move_servo_slowly(ARM_PORT, ARM_STRAIGHT, 5)
	move_servo(CLAW_PORT, CLAW_CLOSED)
	k.create_drive_direct(100, 100)
	k.msleep(10000)
	k.create_disconnect()
def print_battery_info():
	charge = k.get_create_battery_charge()
	capacity = k.get_create_battery_capacity()
	print("Capacity", capacity)
	print("Charge", charge)
	print("Percentage", charge / (capacity if capacity != 0 else charge) * 100)

def place_noodle_on_rack():
	retry_connect(5)
	k.enable_servos()
	#drive forward towards the rack
	drive(150, 150)
	k.msleep(321) #orig 271 for the center right of the rack when facing it
	"""
	#all this is for placing the noodle on the center right of the rack
	ihs_bindings.encoder_turn_degrees_v2(100, -160)
	move_servo_slowly(ARM_PORT, ARM_STRAIGHT, 3)
	"""
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
	turn_to_line_left()
	drive(-100, -100)
	k.msleep(321)
	k.disable_servos()
def get_top_noodle():
	#move_servo_slowly(ARM_PORT, ARM_TOP_NOODLE, 5)
	drive(-50,-50)
	k.msleep(200)
	move_servo(CLAW_PORT, CLAW_CLOSED)
	k.create_stop()
	drive(-45, -45)
	move_servo_slowly(ARM_PORT, ARM_ON_NOODLE_PIPE, 10)
	k.create_stop()
def get_upper_noodle():

	move_servo_slowly(ARM_PORT, ARM_UPPER_NOODLE, 5)

	move_servo(CLAW_PORT, CLAW_CLOSED)
	drive(-45,-45)
	#drive(-10, -10)
	move_servo_slowly(ARM_PORT, ARM_TOP_NOODLE, 5)
	drive(0, 0)
	get_top_noodle()

def get_middle_noodle():

	move_servo_slowly(ARM_PORT, ARM_MIDDLE_NOODLE, 5)

	move_servo(CLAW_PORT, CLAW_CLOSED)
	#drive(-5,-5)# -15
	#drive(-10, -10)
	move_servo_slowly(ARM_PORT, ARM_UPPER_NOODLE, 5)
	drive(0, 0)
	get_upper_noodle()

	k.create_stop()


	k.create_stop()
def get_lower_noodle():
	move_servo_slowly(ARM_PORT, ARM_UPPER_NOODLE, 5)
	k.msleep(1000)
	move_servo(CLAW_PORT, CLAW_CLOSED)
	drive(25,25)
	#drive(-10, -10)
	move_servo_slowly(ARM_PORT, ARM_TOP_NOODLE, 5)
	drive(0, 0)
	get_top_noodle()
def get_bottom_noodle():
	
	move_servo_slowly(ARM_PORT, ARM_LOWER_NOODLE, 5)

	move_servo(CLAW_PORT, CLAW_CLOSED)
	drive(30,30)# -45
	#drive(-10, -10)
	move_servo_slowly(ARM_PORT, ARM_MIDDLE_NOODLE, 5)
	drive(0, 0)
	get_middle_noodle()

	k.create_stop()
def turn_to_line_right():
	#move_servo_slowly(ARM_PORT, ARM_DOWN, 10)
	k.msleep(500)
	while (k.analog(ARM_TOPHAT_PORT) < ROD_TOPHAT_BLACK):
		drive(60,-60)
	k.create_stop()
	k.msleep(500) #give a second for roomba to actually stop
	while (k.analog(ARM_TOPHAT_PORT) > ROD_TOPHAT_BLACK):
		drive(-60, 60)

def grab_turn():
	ihs_bindings.encoder_turn_degrees_v2(300, 180)
	#this is unfinished it has to put it on the rack
	drive(-70,-70)
	k.msleep(1400)

	move_servo(CLAW_PORT, CLAW_OPEN)
	k.msleep(500)
	drive(0,0)

	ihs_bindings.encoder_turn_degrees_v2(300,90)
	drive(-100,-100)
	k.msleep(1000)
	drive(0,0)
	drive_to_line(100,100,left_side,right_side)
	drive_to_line_white(100,100,left_side,right_side)
	
	drive(0,0)
	
	drive(100,100)
	k.msleep(200)

	ihs_bindings.encoder_turn_degrees_v2(300,80)
	#move_servo(ROD_PORT, ROD_LINE)
	
	#move_servo_slowly(ARM_PORT, ARM_DOWN,10)

	k.msleep(500)
	#while k.analog(5) < ROD_TOPHAT_BLACK:
		#drive(0,0)
	#while k.analog(5) > ROD_TOPHAT_BLACK:
		#drive(30, -30)
	#drive(0,0)
	move_servo(ROD_PORT,ROD_LINE)
	move_servo(CLAW_PORT, CLAW_OPEN)
	k.msleep(500) # rod shakes slightly, so we need time to let it settle
	#turn until aligned with the line

	drive(20,-20)
	while (k.analog(ROD_TOPHAT) < ROD_TOPHAT_BLACK):
		continue
	#back up until reaching the line
	#used for alignment
	drive(0, 0)
	"""
	move_servo(ROD_TOPHAT, ROD_LINE - 50) # moves the rod off the line to detect other line
	k.msleep(500)
	drive(30, 30)
	while (k.analog(ROD_TOPHAT) < ROD_TOPHAT_BLACK):
		continue
	drive(0, 0)
	"""
	
	#drive(-10,-10)
	#k.msleep(100)

	#k.msleep(100)
	#move_servo(ARM_PORT, ARM_UPPER_NOODLE)
	#k.msleep(100)
	#drive(-100,-100)
	#k.msleep(850)
	#get_upper_noodle()

def main():
	success = retry_connect(5) ## connects to but, tries 5 times
	if not success:
		print("Failed to connect!!!")
		return -1
	print_battery_info()
	start_time = k.seconds()

	#line up arm with free-standing structure with middle rods
	move_servo_slowly(ARM_PORT, ARM_STRAIGHT_UP, 10) #orig step: 5
	move_servo(CLAW_PORT, CLAW_OPEN)
	ihs_bindings.encoder_turn_degrees_v2(100, -45)
	drive_to_line(200, 200, left_side, right_side) #orig speed: 100, 100
	#ihs_bindings.encoder_turn_degrees_v2(200, 2) #orig speed: 100, -2, deg originally -3 but DO NOT CHANGE since -2 is good
	k.msleep(100)
	drive(-100, -100) #orig speed: -50, -50
	k.msleep(300) #orig time: 500

	k.create_stop()
	drive(-5,-5)
	k.msleep(100)

	#grab free standing structure
	move_servo_slowly(ARM_PORT, ARM_STRAIGHT, 3) ## lowers hand to grab Structure
	k.msleep(100) #orig time: 1000

	move_servo(CLAW_PORT, CLAW_CLOSED) ## closes claw
	k.enable_servos()
	move_servo_slowly(ARM_PORT, ARM_GRAB)
	k.msleep(100) #orig time: 500
	drive(300, 300) #orig speed: 150, 150
	k.msleep(1000) #orig time: 2000

	"""
	#turn out of box
	ihs_bindings.encoder_turn_degrees_v2(100, -20)
	drive(100, 100)
	k.msleep(500)
	"""

	#drive foward to middle of white space
	drive(300, 300) #orig speed: 150, 150
	k.msleep(600) #orig time: 1200
	ihs_bindings.encoder_turn_degrees_v2(100, 90) #orig speed: 50, 90 deg clockwise

	#go to middle line
	#ihs_bindings.encoder_turn_degrees_v2(100, -5)
	"""while (k.analog(BACK_TOPHAT) < 1000):
		drive(-150, -150)"""
	drive_to_line(-150, -150, left_side, right_side) #orig speed: -150, -150
	#drive(100, 100)
	#drive(-150, -150)
	#k.msleep(300)

	#move forward an arbitrary amount to center the roomba on the line (I LOVR HARDCODE>>>>)
	drive(150, 150) #orig speed: 150, 150
	k.msleep(400) #orig time: 400
	drive(0, 0)

	#turn 90 to place structure structure 
	ihs_bindings.encoder_turn_degrees_v2(100, 90) #orig speed: 100, 97 deg clockwise

	#release structure
	move_servo(CLAW_PORT, CLAW_OPEN)
	k.enable_servos()
	move_servo_slowly(ARM_PORT, ARM_STRAIGHT_UP, 10) #orig step: 5
	#drive_to_line(-250, -200, k.get_create_lcliff_amt, k.get_create_rcliff_amt)

	#center on black line
	#while (left_side() and right_side() and left_front() and right_front()) > BLACK and BACK_TOPHAT < BLACK:
	#	drive(100, -100)
	ihs_bindings.encoder_turn_degrees_v2(100,90) #turns 90 to keep sensor on white
	while left_front() > BLACK:
		drive(50,-50)
	while left_front() < BLACK:
		drive(-50,50)
	#ihs_binding .encoder_turn_degrees_v2(100, 100) #orig speed: 100, 165 deg clockwise
	ihs_bindings.encoder_turn_degrees_v2(100,3)
	drive(-150, -150) #orig speed: -150, -150
	k.msleep(500) #orig time: 271

	#INSERT NOODLE GRABBING CODE HERE:
	#noodle garb

	#print the time elapsed since the start of the program
	print("time", k.seconds() - start_time)
	k.create_disconnect()
	k.disable_servos()
#main()
retry_connect(5)
k.create_full()
print_battery_info()
#reset
#move_servo_slowly(ARM_PORT,ARM_TOP_NOODLE,10)
#move_servo_slowly(CLAW_PORT, CLAW_OPEN,10)



start_time = time.time()
move_servo_slowly(CLAW_PORT,CLAW_OPEN,15)
#drives in to get better grip on noodle
"""
button condition
drive(-20, -20)
k.msleep(300)
drive(0, 0)
"""
chew_claw(10)

get_middle_noodle()
grab_turn()
move_servo_slowly(ARM_PORT,ARM_BOTTOM_NOODLE ,10)
#drive(-100,-100)
#k.msleep(850)
#drive(0,0)
#get_bottom_noodle()
#move_servo(ROD_PORT,ROD_SIDE)
#grab_turn()
print(time.time()-start_time)

'''
k.enable_servos()
chew_claw(10)
'''

#move_servo_slowly(CLAW_PORT, CLAW_OPEN,10)
#move_servo_slowly(ARM_PORT, ARM_MIDDLE_NOODLE,10)

'''
i = k.seconds()
chew_claw(5)
get_top_noodle()

#while (k.analog(ARM_TOPHAT_PORT) < ARM_TOPHAT_BLACK):
	#drive(50, -50)
#drive(0, 0)

#start_time = k.seconds()
#while (seconds() - start_time < 1):
	#if (k.analog(ARM_TOPHAT_PORT) > ARM_TOPHAT_BLACK):
		#drive(-60, -30)
	#if (k.analog(ARM_TOPHAT_PORT) < ARM_TOPHAT_BLACK):
		#drive(-30, -60)

grab_turn()
move_servo_slowly(ARM_PORT,ARM_UPPER_NOODLE,10)
drive(-100, -100)
k.msleep(900)
drive(0, 0)	
chew_claw(5)
#move_servo_slowly(ARM_PORT,ARM_ON_NOODLE_PIPE,10)
get_upper_noodle()
move_servo(ROD_PORT,ROD_SIDE)
grab_turn()
move_servo_slowly(ARM_PORT,ARM_MIDDLE_NOODLE,10)
drive(-100,-100)
k.msleep(600)
drive(0,0)
chew_claw(5)
get_middle_noodle()
move_servo(ROD_PORT,ROD_SIDE)
grab_turn()
move_servo_slowly(ARM_PORT,ARM_LOWER_NOODLE,10)
drive(-100,-100)
k.msleep(800)
drive(0,0)
get_lower_noodle()
print((k.seconds()-i)/1000)
'''
'''
line follow
i = k.seconds()
while(i-k.seconds()<1100):
	if k.analog(PLACEHOLDER)<BLACK:
		drive(-10,-5)
	if k.analog(PLACEHOLDER)>BLACK:
		drive(-5,-10)
'''

#move_servo_slowly(ARM_PORT,ARM_STRAIGHT_UP,10)

#move_servo_slowly(ARM_PORT,ARM_ON_NOODLE_PIPE,10)

#drive(-20,-20)
#k.msleep(500)



#chew_claw(5)
#get_middle_noodle()
#get_upper_noodle()
cleanup()

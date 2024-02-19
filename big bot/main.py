from ctypes import CDLL
kipr = "/usr/local/lib/libkipr.so"
k = CDLL(kipr)

import ihs_bindings

CLAW_PORT = 3
ARM_PORT = 1
ARM_TOPHAT_PORT = 0
"""
4176 bot
ARM_STRAIGHT_UP = 1300
ARM_STRAIGHT = 200
ARM_DOWN = 40

CLAW_OPEN = 986
CLAW_CLOSED = 1968
"""
ARM_STRAIGHT_UP = 1300
ARM_STRAIGHT = 200
ARM_GRAB = 100
ARM_DOWN = 40
ARM_ON_RACK = 500

CLAW_OPEN  = 986
CLAW_CLOSED = 1968

SENSOR_BLACK = 3000 ## < SENSORBLACK is white, > SENSORBLACK is black (USE FOR NON-ROOMBA SENSORS)
BLACK = 2600 ## > BLACK is white, < BLACK is black

#sensor shortcuts
def left_side():
	return k.get_create_lcliff_amt()
def left_front():
	return k.get_create_lfcliff_amt()
def right_side():
	return k.get_create_rcliff_amt()
def right_front():
	return k.get_create_rfcliff_amt()
def drive(left_speed, right_speed):
	k.create_drive_direct(left_speed, right_speed)
	return
def farthest_left_distance():
	return k.get_create_llight_bump_amt()
def middle_left_distance():
	return k. get_create_lflightbump_amt()
def foward_left_distance():
	return k.get_create_lclightbump_amt()
def farthest_right_distance():
        return k.get_create_rlight_bump_amt()
def middle_right_distance():
        return k. get_create_rflightbump_amt()
def foward_right_distance():
        return k.get_create_rclightbump_amt()
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
	return False
def cleanup():
	k.create_disconnect()
	k.disable_servos()
# higher step value = faster servo move
# the servo is disabled after calling the function
# to protect microservoes
def move_servo_slowly(port, end_position, step=1):
	start_position = k.get_servo_position(port)
	if end_position == start_position:
		return
	print(start_position)
	if start_position > end_position:
		step = -step
	interval = range(start_position, end_position, step)
	k.enable_servo(port)
	for position in interval:
		k.set_servo_position(port, position)
		k.msleep(10)
	k.disable_servo(port)

# instantly moves servo
# enables servo before moving servo
# disables servo after to protect microservoes
def move_servo(port, end_position):
	k.enable_servo(port)
	k.set_servo_position(port, end_position)
	k.msleep(100)
	k.disable_servo(port)

#square up
def drive_to_line(left_speed, right_speed, left_sensor=left_front, right_sensor=right_front):
	detect = 0
	print (left_sensor(), right_sensor())
	while (left_sensor() > BLACK and right_sensor() > BLACK):
		drive(left_speed, right_speed)
	if detect < 2:
		while (left_sensor() > BLACK):
			drive(left_speed, 0)
		detect += 1
		print (detect)
		while (right_sensor() > BLACK):
			drive(0, right_speed)
		detect += 1
		drive(0,0)
		return

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
	print("Capacity", k.get_create_battery_capacity())
	print("Charge", k.get_create_battery_charge())
	print("Percentage", k.get_create_battery_charge() / k.get_create_battery_capacity() * 100)

def noodle_grab():
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
	move_servo_slowly(ARM_PORT, ARM_DOWN, 10)
	k.msleep(500)
	while (k.analog(ARM_TOPHAT_PORT) < SENSOR_BLACK):
		drive(50, -50)
		print(k.analog(ARM_TOPHAT_PORT))
	drive(-100, -100)
	k.msleep(321)
	k.disable_servos()

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

#main
noodle_grab()
cleanup()

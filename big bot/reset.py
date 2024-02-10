
from ctypes import CDLL
kipr = "/usr/local/lib/libkipr.so"
k = CDLL(kipr)

import ihs_bindings

CLAW_PORT = 0
ARM_PORT = 1
BACK_TOPHAT = 2
"""
4176 bot
ARM_STRAIGHT_UP = 1300
ARM_STRAIGHT = 200
ARM_DOWN = 120

CLAW_OPEN = 986
CLAW_CLOSED = 1968
"""
ARM_STRAIGHT_UP = 1300
ARM_STRAIGHT = 200
ARM_DOWN = 0

CLAW_OPEN  = 986
CLAW_CLOSED = 1968

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

#sensor test
#while True:
#	print (left_side(), "left side")
#	print (" ")
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
def drive_to_line(left_speed, right_speed, left_sensor, right_sensor):
	print(left_sensor(), right_sensor())
	while (left_sensor() > BLACK and right_sensor() > BLACK):
		drive(left_speed, right_speed)
	while (left_sensor() > BLACK):
		drive(left_speed, 0)
	while (right_sensor() > BLACK):
		drive(0, right_speed)
#square up ON WHITE!!!!
def drive_to_line_white(left_speed, right_speed, left_sensor, right_sensor):
	print(left_sensor(), right_sensor())
	while (left_sensor() < BLACK and right_sensor() < BLACK):
		drive(left_speed, right_speed)
	while (left_sensor() < BLACK):
		drive(left_speed, 0)
	while(right_sensor() < BLACK):
		drive(0, right_speed)

def reset():
	k.enable_servos()
	move_servo_slowly(ARM_PORT, ARM_DOWN, 5)
	move_servo(CLAW_PORT, CLAW_CLOSED)
	k.disable_servos()
def line_follow(port, seconds):
	end_time = seconds*1000
	start = k.seconds()
	while (k.seconds() - start < end_time):
		if (k.analog(port) < BLACK):
			k.create_drive_direct(-250, -150)
		if(k.analog(port) > BLACK):
			k.create_drive_direct(-150, -250)
reset()

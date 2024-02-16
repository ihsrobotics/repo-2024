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
ARM_DOWN = 40

CLAW_OPEN = 986
CLAW_CLOSED = 1968
"""
ARM_STRAIGHT_UP = 1300
ARM_STRAIGHT = 200
ARM_GRAB = 100
ARM_DOWN = 40

CLAW_OPEN  = 986
CLAW_CLOSED = 1968

SENSOR_BLACK = 1000 ## < SENSORBLACK is white, > SENSORBLACK is black (USE FOR NON-ROOMBA SENSORS)
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

def main():
	success = retry_connect(5) ## connects to but, tries 5 times
	if not success:
		print("Failed to connect!!!")
		return -1
	start_time = k.seconds()

	#line up arm with free-standing structure left most rods
	move_servo_slowly(ARM_PORT, ARM_STRAIGHT_UP, 5)
	move_servo(CLAW_PORT, CLAW_OPEN)
	ihs_bindings.encoder_turn_degrees_v2(100, -40)
	drive_to_line(100, 100, left_side, right_side)
	ihs_bindings.encoder_turn_degrees_v2(100, -2) #orginally -3
	k.msleep(100)
	drive(-50, -50)
	k.msleep(500)

	k.create_stop()

	#grab free standing structure
	move_servo_slowly(ARM_PORT, ARM_STRAIGHT, 3) ## lowers hand to grab Structure
	k.msleep(1000)

	move_servo(CLAW_PORT, CLAW_CLOSED) ## closes claw
	k.enable_servos()
	move_servo_slowly(ARM_PORT, ARM_GRAB)
	k.msleep(500)
	drive(150, 150)
	k.msleep(2000)

	"""
	#turn out of box
	ihs_bindings.encoder_turn_degrees_v2(100, -20)
	drive(100, 100)
	k.msleep(500)
	"""

	#drive foward to middle of white space
	drive(150, 150)
	k.msleep(1200)
	ihs_bindings.encoder_turn_degrees_v2(50, 90)

	#go to middle line
	#ihs_bindings.encoder_turn_degrees_v2(100, -5)
	"""while (k.analog(BACK_TOPHAT) < 1000):
		drive(-150, -150)"""
	drive_to_line(-150, -150, left_side, right_side)
	#drive(100, 100)
	#drive(-150, -150)
	#k.msleep(300)

	#turn 90 to be able to line follow straight
	ihs_bindings.encoder_turn_degrees_v2(100, 97)
	middle_right_distance()

	#release structure
	move_servo(CLAW_PORT, CLAW_OPEN)
	k.enable_servos()
	move_servo_slowly(ARM_PORT, ARM_STRAIGHT_UP, 5)

	line_follow(left_front, 0.5) ##line follow 2 seconds
	#drive_to_line(-250, -200, k.get_create_lcliff_amt, k.get_create_rcliff_amt)
	print(k.seconds() - start_time)
	k.create_disconnect()
	k.disable_servos()
main()
cleanup()

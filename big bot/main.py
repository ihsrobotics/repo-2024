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
ARM_DOWN = 40

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
def drive_to_line(left_speed, right_speed, left_sensor=left_front, right_sensor=right_front):
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

def line_follow(port, seconds):
	end_time = seconds*1000
	start = k.seconds()
	while (k.seconds() - start < end_time):
		if (k.analog(port) < BLACK):
			k.create_drive_direct(-250, -150)
		if(k.analog(port) > BLACK):
			k.create_drive_direct(-150, -250)
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

	#drive_to_line(-50, -50, k.get_create_lcliff_amt, k.get_create_rcliff_amt)
	start_time = k.seconds()
	
	#line up arm with free-standing structure
	move_servo_slowly(ARM_PORT, ARM_STRAIGHT_UP, 5)
	move_servo(CLAW_PORT, CLAW_OPEN)
	ihs_bindings.encoder_turn_degrees_v2(100, -40)
	drive_to_line(100, 100, left_side, right_side)
	drive_to_line_white(100, 100, right_side, left_side)
	#drive(-50, -50)
	k.msleep(1000)
	#drives to starting line not square up b/c square up makes the bot turn
	"""
	while (left_side() > BLACK and right_side() > BLACK):
		drive(50, 50)
	#drive to make sure both sensors are on the starting line
	drive(50, 50)
	k.msleep(200)
	#drive to the end of the starting line
	while (left_side() < BLACK and right_side() < BLACK):
		drive(50, 50)
	#drive a little past the starting line
	drive(50, 50)
	k.msleep(1000)
	#k.msleep(500) #orginally 1600
	"""
	k.create_stop()

	#grab free standing structure
	move_servo_slowly(ARM_PORT, ARM_STRAIGHT, 3) ## lowers hand to grab Structure
	k.msleep(1000)

	move_servo(CLAW_PORT, CLAW_CLOSED) ## closes claw
	k.enable_servos()
	k.msleep(500)
	drive(150, 150)
	k.msleep(1000)

	#drive_to_line(250, 250, left_front, right_front)
	#ihs_bindings.encoder_drive_straight_cm(-100, 10)
	#drive(250, 250) ##drive past line and out of box
	#k.msleep(500)

	'''#turn out of box
	ihs_bindings.encoder_turn_degrees_v2(100, -20)
	drive(100, 100)
	k.msleep(500)'''

	#drive to second line
	drive_to_line(150, 150, left_side, right_side)
	ihs_bindings.encoder_turn_degrees_v2(50, 180)

	#turn to middle line
	ihs_bindings.encoder_turn_degrees_v2(100, -5)
	while (left_side() > BLACK and right_side() > BLACK):
		drive(150, 150)
	drive_to_line_white(150, 150, left_side, right_side)
	#drive(100, 100)
	k.msleep(300)

	#turn 90 to be able to line follow straight
	ihs_bindings.encoder_turn_degrees_v2(100, -90)

	line_follow(BACK_TOPHAT, 1.5) ##line follow 2 seconds
	#drive_to_line(-250, -200, k.get_create_lcliff_amt, k.get_create_rcliff_amt)
	print(k.seconds() - start_time)
	k.create_disconnect()
	k.disable_servos()
main()


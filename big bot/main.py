from ctypes import CDLL
kipr = "/usr/local/lib/libkipr.so"
k = CDLL(kipr)

import ihs_bindings

CLAW_PORT = 1
ARM_PORT = 0

ARM_STRAIGHT_UP = 1283
ARM_STRAIGHT = 160

CLAW_OPEN  = 986
CLAW_CLOSED = 1968

BLACK = 2600
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
def drive_to_line(left_speed, right_speed, left_sensor, right_sensor):
	print(left_sensor(), right_sensor())
	while (left_sensor() > BLACK and right_sensor() > BLACK):
		k.create_drive_direct(left_speed, right_speed)
	while (left_sensor() > BLACK):
		k.create_drive_direct(left_speed, 0)
	while (right_sensor() > BLACK):
		k.create_drive_direct(0, right_speed)
        
def reset():
	k.enable_servos()
	move_servo_slowly(ARM_PORT, ARM_STRAIGHT_UP, 5)
	move_servo(CLAW_PORT, CLAW_OPEN)
	k.disable_servos()
def line_follow(port, seconds):
	wantedtime = seconds*1000
	start = k.seconds()
	while (k.seconds() - start < wantedtime):
		if (k.analog(port) < BLACK):
			k.create_drive_direct(-250, -150)
		if(k.analog(port) > BLACK):
			k.create_drive_direct(-150, -250)

def main():
	success = retry_connect(5)
	if not success:
		print("Failed to connect!!!")
		return -1
	#drive_to_line(-50, -50, k.get_create_lcliff_amt, k.get_create_rcliff_amt)
	start_time = k.seconds()
	while (k.get_create_lcliff_amt() > BLACK and k.get_create_rcliff_amt() > BLACK):
		k.create_drive_direct(-50, -50)
	k.create_drive_direct(50, 50)
	k.msleep(1600)
	k.create_stop()

	#grab free standing structure
	#move_servo_slowly(ARM_PORT, 672, 10)
	
	move_servo_slowly(ARM_PORT, ARM_STRAIGHT, 3)
	k.msleep(1000)
	move_servo(CLAW_PORT, CLAW_CLOSED)
	k.enable_servos()
	k.msleep(500)
	drive_to_line(-250, -250, k.get_create_lcliff_amt, k.get_create_rcliff_amt)
	#ihs_bindings.encoder_drive_straight_cm(-100, 10)
	k.create_drive_direct(-250, -250)
	k.msleep(500)
	ihs_bindings.encoder_turn_degrees_v2(100, -20)
	k.create_drive_direct(-100, -100)
	k.msleep(800)
	ihs_bindings.encoder_turn_degrees_v2(100, -20)
	drive_to_line(-250, -150, k.get_create_lcliff_amt, k.get_create_rcliff_amt)
	k.create_drive_direct(-100, -100)
	k.msleep(400)
	ihs_bindings.encoder_turn_degrees_v2(100, -90)
	line_follow(2, 3)
	#drive_to_line(-250, -200, k.get_create_lcliff_amt, k.get_create_rcliff_amt)
	print(k.seconds() - start_time)	
	k.create_disconnect()
	k.disable_servos()
#reset()
main()

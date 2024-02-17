import math
from ctypes import CDLL
kipr = "/usr/local/lib/libkipr.so"
import ihs_bindings
k = CDLL(kipr)
CLAW_PORT = 0

#all arm values are for bot 4175
#may change on 4176
ARM_PORT = 1
ARM_DOWN = 116

#arm servo values to grab each of the pipes
#counting from the bottom, the bottom-most is 1
ARM_NOODLE_2 = 250
ARM_STRAIGHT = 315
ARM_UP = 880
CLAW_OPEN = 181
CLAW_CLOSED = 1825
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
def retry_connect(n):
	for i in range(n):
		print("Attempt to connect")
		success = k.create_connect_once()
		if success:
			print("Connected ^w^")
			return True
	print("Not connected :(, check if roomba is on and roomba cable")
	return False
def grab_pipe_noodle_1():
	k.set_servo_position(CLAW_PORT, CLAW_CLOSED)
	k.msleep(500)
	k.set_servo_position(ARM_PORT, ARM_DOWN)
	k.create_drive_direct(50, 50)
	move_servo_slowly(ARM_PORT, ARM_NOODLE_2, 5)
	k.create_stop()
	grab_pipe_noodle_2()
def grab_pipe_noodle_2():
	k.set_servo_position(CLAW_PORT, CLAW_CLOSED)
	k.msleep(500)
	k.set_servo_position(ARM_PORT, ARM_NOODLE_2)
	k.create_drive_direct(50, 50)
	move_servo_slowly(ARM_PORT, ARM_STRAIGHT, 5)
	k.create_stop()
		
	k.create_drive_direct(-30, -30)
	move_servo_slowly(ARM_PORT, ARM_UP - 150, 5)
	
	#bot moves faster towards pipe during the last stretch
	#horizontal distance decreases faster at this point
	
	k.create_drive_direct(-30, -30)
	move_servo_slowly(ARM_PORT, ARM_UP, 3)
	
#move back right away
#450 move foward
#610 move foward again
retry_connect(5)
k.enable_servos()

grab_pipe_noodle_2()
ihs_bindings.encoder_turn_degrees_v2(100, -180)
k.set_servo_position(CLAW_PORT, CLAW_OPEN)
ihs_bindings.encoder_turn_degrees_v2(100, 180)
#grab_pipe_noodle_1()
"""
k.set_servo_position(CLAW_PORT, CLAW_OPEN)
k.msleep(100)
k.set_servo_position(ARM_PORT, ARM_DOWN)
k.msleep(100)
k.set_servo_position(CLAW_PORT, CLAW_CLOSED)
k.msleep(500)
#move servo up and move away from pipe to allow arm to rise
k.create_drive_direct(50, 50)
move_servo_slowly(ARM_PORT, ARM_STRAIGHT, 5)

#raise up in two goes so the noodles dont slip
k.create_drive_direct(-30,-30)
move_servo_slowly(ARM_PORT, math.floor((ARM_UP - ARM_STRAIGHT) / 2 + ARM_STRAIGHT), 5)
k.create_stop()
#wait to let the arm settle
k.msleep(1000)

#move servo up further past horizontal
#move toward pipe to allow arm to rise
k.create_drive_direct(-50,-50)
move_servo_slowly(ARM_PORT, ARM_UP, 5)
"""

k.create_stop()
k.create_disconnect()

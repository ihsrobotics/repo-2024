from ctypes import CDLL
kipr = "/usr/local/lib/libkipr.so"
k = CDLL(kipr)

import ihs_bindings
import sys
import math
import time

sys.path.append("/home/pi/Documents/IME_files/purpleNoodle/include")
from sensorshortcuts import *
from constants import *


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

def print_battery_info():
	charge = k.get_create_battery_charge()
	capacity = k.get_create_battery_capacity()
	if (capacity == 0 or charge == 0 or charge > capacity):
		print("Battery info is invalid, try again later")
		return False
	print("Capacity", capacity)
	print("Charge", charge)
	print("Percentage", charge / (capacity if capacity != 0 else 1) * 100)
	return True

def drive_to_line(left_speed, right_speed, left_sensor=left_front, right_sensor=right_front):
	print (left_sensor(), right_sensor())
	while (left_sensor() >= BLACK and right_sensor() >= BLACK):
		drive(left_speed, right_speed)
	while (left_sensor() >= BLACK):
		drive(left_speed, 0)
	while (right_sensor() >= BLACK):
		drive(0, right_speed)
	while (left_sensor() >= BLACK):
		drive(left_speed, 0)
	drive(0,0)
	return
def drive_to_line_white(left_speed, right_speed, left_sensor, right_sensor):
	print (left_sensor(), right_sensor())
	while (left_sensor() <= BLACK and right_sensor() <= BLACK):
		drive(left_speed, right_speed)
	while (left_sensor() <= BLACK):
		drive(left_speed, 0)
	while(right_sensor() <= BLACK):
		drive(0, right_speed)
	return

def move_servo(port, end_position):
	k.enable_servo(port)
	k.set_servo_position(port, end_position)
	k.msleep(100)

def move_servo_slowly(port, end_position, delay=0):
	k.enable_servo(port)
	position = k.get_servo_position(port)
	if end_position == position:
	    return
	elif delay == 0:
	    k.set_servo_position(port, end_position)
	    k.msleep(100)
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

def go_to_switch():
    ihs_bindings.encoder_turn_degrees_v2(100, 180)
def is_right_front_white():
	return right_front() > BLACK
def is_left_side_white():
	return left_side() > BLACK
def is_rod_white():
	return k.analog(ROD_PORT) < ROD_TOPHAT_BLACK
def line_follow(sensor_port, continue_condition = is_right_front_white):
	while continue_condition():
		print(k.analog(ROD_PORT))
		if k.analog(sensor_port) <= SWEEPER_BLACK:
			drive(-25, -125)
		elif k.analog(sensor_port) >= SWEEPER_BLACK:
			drive(-125,-25)

def main():
	"""
	success = retry_connect(5) ## connects to but, tries 5 times
	if not success:
		print("Failed to connect!!!")
		return -1
	"""
	if not print_battery_info():
		print("invalid battery info probably means bot will do something dumb")
		return -1
	start_time = k.seconds()

	#line up arm with free-standing structure with middle rods
	move_servo_slowly(ARM_PORT, ARM_STRAIGHT, 5) 
	k.msleep(200)
	
	print("servo should've moved")
	drive(-100, -100)
	k.msleep(500)
	drive(0, 0)
	#move_servo_slowly(ROD_PORT, ROD_LEFT_SIDE, 5)
	ihs_bindings.encoder_turn_degrees_v2(100,-45)
	drive_to_line(200, 200, left_side, right_side)
	drive_to_line_white(150, 150, left_side, right_side)
	k.msleep(100)



	drive(500, 500) #orig speed: 150, 150
	k.msleep(1000) #orig time: 1200
	ihs_bindings.encoder_turn_degrees_v2(100, -90) #orig speed: 50, 90 deg clockwise

	#go to middle line
	#ihs_bindings.encoder_turn_degrees_v2(100, -5)

	drive_to_line(150, 150, left_side, right_side)

	drive(300,300)
	k.msleep(100)

	ihs_bindings.encoder_turn_degrees_v2(100,90)
	drive_to_line(150, 150, left_side, right_side)
	k.msleep(100)
	drive_to_line_white(150,150, left_side, right_side)
	drive(0,0)
	
	move_servo(ROD_PORT,ROD_STRAIGHT)
	ihs_bindings.encoder_turn_degrees_v2(100,95)
	k.msleep(300)
	
	#turns toward switch
	drive(-30,30)
	while k.analog(ROD_TOPHAT)  <= ROD_TOPHAT_BLACK:
		pass
	drive(0,0)
	
	move_servo_slowly(ROD_PORT,ROD_SIDE,5)
	move_servo_slowly(ARM_PORT, ARM_DOWN, 5)
	#drives to switch
	line_follow(SWEEPER_TOPHAT_PORT)
	drive(0,0)

	#flips switch UP
	#currently flips switch down
	move_servo(ARM_PORT,ARM_MIDDLE_NOODLE)

	ihs_bindings.encoder_turn_degrees_v2(100,170)
	#drive(-300,-300)
	#k.msleep(200)
	line_follow(SWEEPER_TOPHAT_PORT, is_left_side_white)
	drive(0, 0)
	move_servo(ROD_PORT, ROD_STRAIGHT)
	drive(30,-30)
	while k.analog(ROD_TOPHAT) <= ROD_TOPHAT_BLACK:
		pass
	drive(0,0)

	
retry_connect(5)
print_battery_info()
#line_follow(SWEEPER_TOPHAT_PORT)
#move_servo_slowly(ARM_PORT,ARM_DOWN)
k.enable_servos()
"""
while True:
	k.msleep(1000)
	print(right_front())
"""
#drive(0,0)
#drive_to_line_white(150,150, left_side, right_side)
main()
#ihs_bindings.encoder_turn_degrees_v2(100,180)

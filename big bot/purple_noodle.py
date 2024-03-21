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
	print("Capacity", capacity)
	print("Charge", charge)
	print("Percentage", charge / (capacity if capacity != 0 else charge) * 100)

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
	k.disable_servo(port)

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

def go_to_switch():
    ihs_bindings.encoder_turn_degrees_v2(100, 180)
    
def main():
	success = retry_connect(5) ## connects to but, tries 5 times
	if not success:
		print("Failed to connect!!!")
		return -1
	print_battery_info()
	start_time = k.seconds()

	#line up arm with free-standing structure with middle rods
	move_servo_slowly(ARM_PORT, ARM_STRAIGHT, 5) 
	k.msleep(200)
	drive(-100, -100)
	k.msleep(500)
	drive(0, 0)
	move_servo_slowly(ROD_PORT, ROD_LEFT_SIDE, 5)
	ihs_bindings.encoder_turn_degrees_v2(100,-45)
	drive_to_line(200, 200, left_side, right_side)
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
	


main()

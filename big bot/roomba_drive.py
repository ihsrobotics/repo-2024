from ctypes import CDLL
kipr = "/usr/local/lib/libkipr.so"
k = CDLL(kipr)

from sensor_shortcuts import *
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

def drive_to_line(left_speed, right_speed, left_sensor=left_front, right_sensor=right_front):
	print (left_sensor(), right_sensor())
	while (left_sensor() >= BLACK and right_sensor() >= BLACK):
		drive(left_speed, right_speed)
	for i in range(2):
	    while (left_sensor() >= BLACK):
	    	drive(left_speed, 0)
	    while (right_sensor() >= BLACK):
		    drive(0, right_speed)
	drive(0,0)
	return
def drive_to_line_white(left_speed, right_speed, left_sensor, right_sensor):
	print (left_sensor(), right_sensor())
	while (left_sensor() <= BLACK and right_sensor() <= BLACK):
		drive(left_speed, right_speed)
	for i in range(2):
	    while (left_sensor() <= BLACK):
	    	drive(left_speed, 0)
	    while (right_sensor() <= BLACK):
		    drive(0, right_speed)
	return
def line_follow(sensor_port, continue_condition):
	while continue_condition():
		if k.analog(sensor_port) <= SWEEPER_BLACK:
			drive(-100, -125)
		elif k.analog(sensor_port) >= SWEEPER_BLACK:
			drive(-125,-100)
def rod_align_black(left_speed, right_speed):
	drive(left_speed, right_speed)
	while k.analog(ROD_TOPHAT) <= ROD_TOPHAT_BLACK:
		pass
	drive(0, 0)
def rod_align_white(left_speed, right_speed):
	drive(left_speed, right_speed)
	while k.analog(ROD_TOPHAT) >= ROD_TOPHAT_BLACK:
		pass
	drive(0, 0)
def sweeper_align_black(left_speed, right_speed):
    drive(left_speed, right_speed)
    while k.analog(SWEEPER_TOPHAT_PORT) <= SWEEPER_BLACK:
        pass
    drive(0, 0)

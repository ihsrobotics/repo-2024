from ctypes import CDLL
kipr = "/usr/local/lib/libkipr.so"
k = CDLL(kipr)

import ihs_bindings
import sys
import math

sys.path.append("/home/pi/Documents/IME_files/purpleNoodle/include")
from roomba_drive import *



def print_battery_info():
	print("Controller Battery:", k.power_level_nimh())
	charge = k.get_create_battery_charge()
	capacity = k.get_create_battery_capacity()
	if (capacity == 0 or charge == 0 or charge > capacity):
		print("Battery info is invalid, try again later")
		return False
	print("Roomba Capacity:", capacity)
	print("Roomba Charge:", charge)
	print("Roomba Percentage:", str(charge / (capacity if capacity != 0 else 1) * 100) + "%")
	return True

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

def is_right_front_white():
	return right_front() > BLACK
def is_left_side_white():
	return left_side() > BLACK
def is_right_side_white():
	return right_side() > BLACK
def is_rod_white():
	return k.analog(ROD_PORT) > ROD_TOPHAT_BLACK
def sweep():
	speed = -1000
	k.mav(SWEEPER_PORT, speed)
	k.msleep(600)
	k.mav(SWEEPER_PORT, -speed)
	k.msleep(600)
	k.mav(SWEEPER_PORT, 0)
def main():
	"""
	while right_side() > BLACK:
		drive(-200,-200)
		print(right_side())
	drive(0,0)
	"""
	if not print_battery_info():
		print("invalid battery info probably means bot will do something dumb")
		return -1
	start_charge = k.get_create_battery_charge()
	#line up arm with free-standing structure with middle rods
	move_servo_slowly(ARM_PORT, ARM_STRAIGHT_UP, 3) 
	k.msleep(200)
	
	drive(-100, -100)
	k.msleep(500)
	drive(0, 0)
	#move_servo_slowly(ROD_PORT, ROD_LEFT_SIDE, 5)
	ihs_bindings.encoder_turn_degrees_v2(500,-45)
	drive_to_line(250, 250, left_side, right_side)
	#drive_to_line_white(300, 300, left_side, right_side)
	k.msleep(100)

	start_time = time()
	drive(500, 500) #orig speed: 150, 150
	k.msleep(1100) #orig time: 1200
	ihs_bindings.encoder_turn_degrees_v2(500, -90) #orig speed: 50, 90 deg clockwise

	#go to middle line
	#ihs_bindings.encoder_turn_degrees_v2(100, -5)

	drive_to_line(250, 250, left_side, right_side)
	drive(300,300)
	k.msleep(100)
	
	ihs_bindings.encoder_turn_degrees_v2(500,90)
	#sweep()
	drive_to_line(300, 300, left_side, right_side)
	drive_to_line_white(150,150, left_side, right_side)
	drive(0,0)

	#drives towards cubes
	ihs_bindings.encoder_turn_degrees_v2(100, 90)
	
	#drive towards tower
	sweeper_align_black(30, -30)
	move_servo(ROD_PORT, 1800) #position rod so line follow is precise, og: 1285
	k.msleep(500) # wait for rod to settle down
	
	def is_rod_black():
		return k.analog(ROD_TOPHAT) < ROD_TOPHAT_BLACK
	#line_follow(SWEEPER_TOPHAT_PORT, is_rod_black)
	
	#does the same thing as the line

	line_follow(SWEEPER_TOPHAT_PORT, is_rod_black)
	drive(0,0)
	'''
	drive(-200,-200)
	
	while right_side() > BLACK:
		pass
	drive(0,0)
	move_servo_slowly(ARM_PORT, ARM_SWITCH_UP,10)
	
	drive(100,100)
	k.msleep(150)


    
    #pick up cubes
	drive(200,200)
	k.msleep(100)



	drive(0,0)
	move_servo_slowly(ARM_PORT,ARM_SHELF-10,10)
	k.msleep(100)
	move_servo_slowly(CLAW_PORT, CLAW_CLOSED, 10)
	k.msleep(500)
	move_servo_slowly(ARM_PORT, ARM_STRAIGHT_UP, 5)
	
	#drops off cubes
	ihs_bindings.encoder_turn_degrees_v2(500, -135)
	move_servo_slowly(ARM_PORT, ARM_DOWN,5)
	move_servo(CLAW_PORT, CLAW_OPEN)
	ihs_bindings.encoder_turn_degrees_v2(500, 130)
	move_servo_slowly(ARM_PORT, ARM_STRAIGHT_UP, 5)
	line_follow(SWEEPER_TOPHAT_PORT, is_rod_black)
	line_follow(SWEEPER_TOPHAT_PORT, is_rod_white)
	print("done")
	'''

	#turn towards drawer
	
	ihs_bindings.encoder_turn_degrees_v2(500, -33)
	
	move_servo(CLAW_PORT, 100)

	move_servo_slowly(ARM_PORT, ARM_DOWN - 20, 5)

	k.msleep(500)


	move_servo(CLAW_PORT, CLAW_DRAWER)
	#drive into handle
	drive(100,100)
	while right_side() < BLACK:
		pass
	k.msleep(200)#0g: 170
	drive(0, 0)
	#re adjust
	ihs_bindings.encoder_turn_degrees_v2(100, 3)
	ihs_bindings.encoder_turn_degrees_v2(100, -2)
	

	#k.msleep(1000)
	ihs_bindings.encoder_turn_degrees_v2(50, -3)
	drive(-25, -25)
	k.msleep(100)
	drive(0, 0)
	#k.msleep(1000)
	#re adjust
	move_servo(CLAW_PORT, CLAW_DRAWER + 15)
	ihs_bindings.encoder_turn_degrees_v2(50, -10)
	ihs_bindings.encoder_turn_degrees_v2(50, 2)
	drive(50, 50)
	k.msleep(100)
	ihs_bindings.encoder_turn_degrees_v2(50, -10)
	ihs_bindings.encoder_turn_degrees_v2(50, 2)
	drive(50, 50)
	k.msleep(100)
	ihs_bindings.encoder_turn_degrees_v2(50, -5)
	return
	"""
	drive(50, 50)
	k.msleep(100)
	drive(0, 0)
	ihs_bindings.encoder_turn_degrees_v2(50, -10)
	"""
	#release drawer
	drive(-200,-200)
	k.msleep(350)
	drive(0,0)
	move_servo_slowly(ARM_PORT,ARM_STRAIGHT_UP, 10)
	#ihs_bindings.encoder_turn_degrees_v2(100,45)
	#drive back 
	drive(500, 500)
	k.msleep(550)
	ihs_bindings.encoder_turn_degrees_v2(200, -20)
	# Drive to mid line 
	drive_to_line(-100, -100, left_side, right_side)
	drive(-500, -500)
	k.msleep(300)
	drive_to_line(100, 100, left_side, right_side)
	drive_to_line_white(100, 100, left_side, right_side)
	drive(0, 0)
	move_servo_slowly(ARM_PORT, ARM_DOWN, 5)
	move_servo_slowly(CLAW_PORT, CLAW_OPEN, 5)
	ihs_bindings.encoder_turn_degrees_v2(200, 80)
	sweeper_align_black(30, -30)
	#drive to switch
	drive(0, 0)
	k.msleep(500)
	line_follow(SWEEPER_TOPHAT_PORT, is_right_front_white)
	drive(0, 0)
	#flick up
	move_servo(ARM_PORT, ARM_SWITCH_UP)

	k.msleep(500)

	drive(300,300)
	k.msleep(500)
	move_servo_slowly(ARM_PORT, ARM_SHELF, 5)
	#drives towards cubes
	line_follow(SWEEPER_TOPHAT_PORT, is_right_side_white)
	'''
	drive(-200,-200)
	
	while right_side() > BLACK:
		pass
	drive(0,0)
	'''
	drive(100,100)
	k.msleep(150)


    
    #pick up cubes
	drive(200,200)
	k.msleep(100)



	drive(0,0)
	#move_servo_slowly(ARM_PORT,ARM_SHELF-10,10)
	k.msleep(100)
	move_servo_slowly(CLAW_PORT, CLAW_CLOSED, 10)
	k.msleep(500)
	move_servo_slowly(ARM_PORT, ARM_STRAIGHT_UP, 5)
	
	#drops off cubes
	ihs_bindings.encoder_turn_degrees_v2(500, -135)
	move_servo_slowly(ARM_PORT, ARM_DOWN,5)
	move_servo(CLAW_PORT, CLAW_OPEN)
	ihs_bindings.encoder_turn_degrees_v2(500, 130)
	move_servo_slowly(ARM_PORT, ARM_STRAIGHT_UP, 5)
	line_follow(SWEEPER_TOPHAT_PORT, is_rod_black)
	line_follow(SWEEPER_TOPHAT_PORT, is_rod_white)\
	#print("done")
    
	
	'''
	#DO NOT DELETE
	#move_servo(ROD_PORT,ROD_STRAIGHT)
	ihs_bindings.encoder_turn_degrees_v2(500,80)
	k.msleep(100)
	drive_to_line(200,200,left_side, right_side)
	#turns toward switch
	sweeper_align_black(30, -30)
	sweep()
	move_servo(ROD_PORT, ROD_SIDE)
	move_servo_slowly(ARM_PORT, ARM_DOWN, 3)

	#drives to switch
	line_follow(SWEEPER_TOPHAT_PORT, is_right_front_white)
	drive(0, 0)
	#one more alignment for good measure
	move_servo(ROD_PORT,ROD_STRAIGHT)
	k.msleep(500)
	rod_align_black(-30, 30)
	rod_align_white(30, -30)
	drive(0,0)
	move_servo(ROD_PORT, ROD_SIDE)
	drive(50, 50)
	k.msleep(200)
	drive(0,0)

	#flips switch UP
	move_servo(ARM_PORT,ARM_SWITCH_UP)
    
	k.msleep(500) #servo jitters, give it a second to flip switch
	drive(20, 20)
	k.msleep(400)
	drive(0, 0)
	move_servo_slowly(ARM_PORT, ARM_LAVA_RESET, 3)

    #turn around and grab yannis
	move_servo(ROD_PORT, ROD_STRAIGHT)
	ihs_bindings.encoder_turn_degrees_v2(500,175)
	#drive(-300,-300)
	#k.msleep(200)
	#line_follow(SWEEPER_TOPHAT_PORT, is_left_side_white)
	drive(0, 0)
	rod_align_black(50, -50)
	rod_align_white(-50, 50)
	
	move_servo(ROD_PORT, 1300) # moves sensor so we can detect the side line (original: 1370)
	k.msleep(500) # give time for rod to settle down for more accurate sensor
	rod_align_black(-100, -100)
	drive(0, 0)
	move_servo(ROD_PORT, ROD_SIDE)
	ihs_bindings.encoder_turn_degrees_v2(200, -5)
	move_servo(CLAW_PORT, CLAW_CLOSED)
	ihs_bindings.encoder_turn_degrees_v2(200, 60)

	#shakes the purple tubes off the base
	move_servo_slowly(ARM_PORT, ARM_MIDDLE_NOODLE)	
	for i in range(2):
		drive(50, 50)
		k.msleep(200)
		drive(-50, -50)
		k.msleep(200)
    # move roomba sensors off line to realign
	drive(500, 500)
	k.msleep(200)
	drive_to_line(-150, -150, left_side, right_side)
	drive(500, 500)
	k.msleep(200)
	drive(0, 0)
	#moves arm up to clear avoid hitting structure
	move_servo_slowly(ARM_PORT, ARM_STRAIGHT_UP, 3)
	ihs_bindings.encoder_turn_degrees_v2(100, -100)

	#moves onto line for line follow
	drive(-300, -300)
	while k.analog(SWEEPER_TOPHAT_PORT) <= SWEEPER_BLACK:
		pass
	while k.analog(SWEEPER_TOPHAT_PORT) >= SWEEPER_BLACK:
		pass
	k.msleep(300)
	drive(-200, 200)
	while k.analog(SWEEPER_TOPHAT_PORT) <= SWEEPER_BLACK:
		pass
	drive(0, 0)
	sweep()
	"""
	'''
	print("Time:", time() - start_time)
	print("Roomba Battery Used", str((k.get_create_battery_charge() - start_charge)/k.get_create_battery_capacity() * 100) + "%")
	#move_servo_slowly(ARM_PORT, ARM_LAVA_RESET, 5)
	

if __name__ == "__main__":
	retry_connect(5)
	print_battery_info()
	k.create_safe()
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

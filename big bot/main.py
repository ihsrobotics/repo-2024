from ctypes import CDLL
kipr = "/usr/local/lib/libkipr.so"
k = CDLL(kipr)

CLAW_PORT = 0
ARM_PORT = 1

ARM_STRAIGHT = 360

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
	print("function called")
	start_position = k.get_servo_position(port)
	if end_position == start_position:
		print("positions are equal")
		return
	print(start_position)
	if start_position > end_position:
		step = -step
	interval = range(start_position, end_position, step)
	print("interval: ", interval)
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
	while (left_sensor() > BLACK or right_sensor() > BLACK):
		k.create_drive_direct(left_speed, right_speed)
	while (left_sensor() > BLACK):
		k.create_drive_direct(left_speed, 0)
	while (right_sensor() > BLACK):
		k.create_drive_direct(0, right_speed)
def main():
	success = retry_connect(5)
	if not success:
		print("Failed to connect!!!")
		return -1
	drive_to_line(-100, -100, k.get_create_lcliff_amt, k.get_create_rcliff_amt)
	k.create_drive_direct(100, 100)
	k.msleep(500)
	k.create_stop()
	move_servo_slowly(ARM_PORT, ARM_STRAIGHT, 50)
	move_servo(CLAW_PORT, CLAW_CLOSED)
	k.create_drive_direct(-50, -50)
	k.msleep(1000)
	k.create_disconnect()
	k.disable_servos()

main()

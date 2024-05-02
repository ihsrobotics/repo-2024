import sys
sys.path.append("/home/pi/Documents/IME_files/start_seq/include")
from bot_functions import *
from config_loader import *

print('Running...')

SERVO = 1

k.enable_servo(SERVO)
k.set_servo_position(SERVO, 2047)
k.msleep(100)
k.disable_servo(SERVO)

is_open = False

while k.digital(RIGHT_BUTTON) != 1:
    if k.digital(LEFT_BUTTON) == 1:
        k.enable_servo(SERVO)
        if is_open: 
            k.set_servo_position(SERVO, 2047)
        else:
            k.set_servo_position(SERVO, 0)
        k.msleep(100)
        k.disable_servo(SERVO)
        is_open = not is_open
        k.msleep(2900)
    k.msleep(100)

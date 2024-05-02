import sys
sys.path.append("/home/pi/Documents/IME_files/Small_bot_4174/include")
from bot_functions import *
from config_loader import *

print('Running...')

k.enable_servo(0)
k.set_servo_position(0, 2047)
k.msleep(100)
k.disable_servo(0)

is_open = False

while k.digital(RIGHT_BUTTON) != 1:
    if k.digital(LEFT_BUTTON) == 1:
        k.enable_servo(0)
        if is_open: 
            k.set_servo_position(0, 2047)
        else:
            k.set_servo_position(0, 0)
        k.enable_servo(0)
        is_open = not is_open
        k.msleep(3000)
    k.msleep(100)

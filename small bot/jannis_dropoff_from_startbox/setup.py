import sys
sys.path.append("/home/pi/Documents/IME_files/Small_bot_4174/include")
from bot_functions import *
from config_loader import *

def setup():
    set_arm_pos(0)
    k.set_servo_position(JANNIS_SERVO, 380)
    k.msleep(100)
    k.set_servo_position(BOOM_SERVO, 1600)
    k.msleep(100)

if __name__ == "__main__":
    k.enable_servos()
    setup()
    k.disable_servos()

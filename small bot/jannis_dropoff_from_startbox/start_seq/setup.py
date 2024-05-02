import sys
sys.path.append("/home/pi/Documents/IME_files/start_seq/include")
from bot_functions import *
from config_loader import *

def setup():
    k.set_servo_position(CLAW_SERVO, CLAW_COMB_CLOSE_POS)
    k.msleep(100)
    k.set_servo_position(JANNIS_SERVO, JANNIS_DOWN_POS)
    k.msleep(100)
    k.set_servo_position(BOOM_SERVO, 175)
    k.msleep(100)
    while k.analog(SLIDE) > ARM_UP_POS:
        k.mav(ARM, -1500)
    stop_motor(ARM)

if __name__ == "__main__":
    k.enable_servos()
    setup()
    k.disable_servos()

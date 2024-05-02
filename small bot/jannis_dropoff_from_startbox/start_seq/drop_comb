import sys
sys.path.append("/home/pi/Documents/IME_files/start_seq/include")
from bot_functions import *
from config_loader import *
from time import time

def drop_astronaut_claw():
    k.set_servo_position(CLAW_SERVO, 1300)
    k.msleep(100)

    while k.analog(SLIDE) < ARM_DOWN_POS:
        k.mav(ARM, 1500)
    stop_motor(ARM)
    k.mav(ARM, 1500)
    k.msleep(200)
    stop_motor(ARM)
    k.mav(RIGHT_WHEEL, -1000)
    
    for i in range(2):
        
        #Move Arm Up
        k.mav(ARM, -1150)
        k.msleep(500)
        stop_motor(ARM)

        #Move Arm Down
        k.mav(ARM, 1150)
        k.msleep(500)
        stop_motor(ARM)
    #Move Arm Up
    k.mav(ARM, -1150)
    k.msleep(500)
    stop_motor(ARM)
    brake()

if __name__ == "__main__":
    timer = time()
    k.enable_servos()
    drop_astronaut_claw()
    k.disable_servos()
    print("Runtime in secs:", time() - timer)

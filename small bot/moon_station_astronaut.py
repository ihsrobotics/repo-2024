import sys
sys.path.append("/home/pi/Documents/IME_files/Small_bot_4174/include")
from bot_functions import *
from config_loader import *

# set up on left side of the horizontal line from the solar panel facing west

def go_to_middle():
    set_arm_pos(450)
    k.set_servo_position(BOOM_SERVO, BOOM_RIGHT_POS)
    k.msleep(100)

    while not on_tape(FRONT_TOPHAT, FRONT_BLACK):
        line_follow(1200, 1500, "RIGHT", BOOM_TOPHAT, BOOM_BLACK)
    brake()

    while on_tape(FRONT_TOPHAT, FRONT_BLACK):
        drive(1500,1500)
    brake()

    drive(1000, 1000, 550)
    brake()

    k.set_servo_position(BOOM_SERVO, 900)
    k.msleep(100)

    while not on_tape(BOOM_TOPHAT, BOOM_BLACK):
        drive(570, -525)
    brake()

def drop_em():
    k.msleep(700)
    
    k.mav(ARM, -500)
    k.msleep(500)

def main():
    go_to_middle()
    drop_em()



if __name__ == "__main__":
    k.enable_servos()
    main()

    k.disable_servos()

import sys
sys.path.append("/home/pi/Documents/IME_files/Small_bot_4174/include")
from bot_functions import *
from config_loader import *

def setup():
    k.set_servo_position(JANNIS_SERVO, 1000)
    k.msleep(100)
    k.set_servo_position(BOOM_SERVO, 1740)
    k.msleep(100)

def clasp_jannis():
    k.set_servo_position(BOOM_SERVO, 500)
    k.msleep(100)
    while (k.analog(SLIDE) > 960):
        k.mav(ARM, -300)
    stop_motor(ARM)

    # drive(300, 550, 750) # 300, 500, 780
    drive(150, 275, 1500)
    brake()

    # while k.get_servo_position(JANNIS_SERVO) > 400:
    #     k.set_servo_position(JANNIS_SERVO, k.get_servo_position(JANNIS_SERVO) - 10)
    #     k.msleep(5)

    # k.msleep(1000)
    
    while k.get_servo_position(JANNIS_SERVO) > 250:
        k.set_servo_position(JANNIS_SERVO, k.get_servo_position(JANNIS_SERVO) - 10)
        k.msleep(5)
    k.disable_servo(JANNIS_SERVO)


def drop_limbs():
    drive(-1500, -1500, 100)
    brake()
    drive(1500, 1500, 50)

def drive_to_dropoff():
    # drive(1500,800,1000)
    # k.set_servo_position(BOOM_SERVO, BOOM_RIGHT_POS)
    # while not on_tape(FRONT_TOPHAT, FRONT_BLACK):
    #     k.line_follow(1200,1500, "LEFT", BOOM_TOPHAT, BOOM_BLACK)

    print(k.analog(BOOM_TOPHAT))
    while not on_tape(BOOM_TOPHAT, BOOM_BLACK):
        drive(1500, 750)
    brake()

    k.msleep(1000) # wait for drops

    while not on_tape(BOOM_TOPHAT, BOOM_BLACK):
        drive(1500, 200)
    while on_tape(BOOM_TOPHAT, BOOM_BLACK):
        drive(1500, 200)
    brake()



def main():
    clasp_jannis()
    k.msleep(500)
    drop_limbs()
    # k.msleep(1000) # wait for drops
    # drive_to_dropoff()
    
if __name__ == "__main__":
    k.enable_servos()
    main()
    k.disable_servos()

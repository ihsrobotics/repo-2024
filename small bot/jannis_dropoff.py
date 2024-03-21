import sys
sys.path.append("/home/pi/Documents/IME_files/lava_tube_poms/include")
from bot_functions import *
from config_loader import *



def main():
    #Back into black tape
    while k.analog(FRONT_TOPHAT) < BLACK:
        drive(-500, -500)
    brake()

    #Line follow for 4.725 seconds to bring jannis under the tube
    start = k.seconds()
    while k.seconds() < start + 5000:
        line_follow(500, 700, "RIGHT", BOOM_BLACK, BOOM_TOPHAT)
    brake()

    #Move the left wheel back to straighten out jannis
    drive(-200, 0)
    k.msleep(700)
    brake()

    #Release Jannis
    for i in range (k.get_servo_position(JANNIS), 2047):
        k.set_servo_position(JANNIS, i)
        k.msleep(1)
    
    

if __name__ == "__main__":
    raise_arm()
    k.enable_servos()
    k.set_servo_position(BOOM_ARM, 2047)
    k.set_servo_position(JANNIS, LOWER_JANNIS)
    k.set_servo_position(LEVER_SERVO, 2047)

main()



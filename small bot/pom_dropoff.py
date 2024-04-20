import sys
sys.path.append("/home/pi/Documents/IME_files/lava_tube_poms/include")
from bot_functions import *
from config_loader import *



def unload_poms():
        for i in range(7):
                #Run Drill For a Second
                k.mav(DRILL, -550)
                

                #Swipe With Swiper
                k.set_servo_position(SWIPER, 990)
                k.msleep(4000)

                for i in range(k.get_servo_position(SWIPER), 433, -1):
                        k.set_servo_position(SWIPER, i)
                k.msleep(200)
                    
        stop_motor(DRILL)

def main():

        # #Turn Around
        # turn_90("LEFT")
        # turn_90("LEFT")

        # #Swing Boom to Right Side of Tape
        # k.set_servo_position(BOOM_ARM, 0)
        # k.msleep(1000)

        # #Drive Until the Bot Passes the Tape
        # while not on_tape():
        #         drive(1000, 1000)
        # while on_tape():
        #         drive(1000, 1000)
        # brake()


        # #Line Follow Until Center Tape
        # arm_position = k.get_servo_position(BOOM_ARM)
        # while not on_tape(BOOM_TOPHAT):
        #         line_follow(500, 900, "RIGHT")
        # brake()

        # #Pass the Tape
        # while on_tape(BOOM_TOPHAT):
        #         drive(1000, 1000)

        # #Turn Toward Moon Base
        # turn_90("RIGHT")

        # #Swing Boom to Left Side of Tape
        # k.set_servo_position(BOOM_ARM, 2047)
        # k.msleep(1000)

        # #Line Follow Until Front Tophat Reaches Tape
        # while not on_tape():
        #         line_follow(500, 700, "LEFT", BOOM_BLACK, BOOM_TOPHAT)
        # brake()
        # print("REACHED TAPE")

        # #Swing Boom to Drawer Angle
        # k.set_servo_position(BOOM_ARM, 330)
        # k.msleep(1000)

        # #Turn Until Boom Reaches Tape
        # while not on_tape(BOOM_TOPHAT):
        #         drive(0, 500)
        # brake()

        # lower_arm()


        #---------------------------------------


        #Turn Toward Solar Panel Tape
        turn_90("LEFT")

        #Drive Until Front Tophat Reaches Tape
        while not on_tape():
                drive(1000, 1000)
        brake()

        #Turn Toward Center Tape
        turn_90("LEFT")

        #Swing Boom Onto Left Side
        k.set_servo_position(BOOM_ARM, 2047)
        k.msleep(1000)

        #Line Follow Until Boom Tophat Reaches Tape
        while not on_tape(BOOM_TOPHAT):
                line_follow(500, 900, "LEFT")
        brake()

        #Swing Boom to Drawer Angle
        k.set_servo_position(BOOM_ARM, 630)
        k.msleep(1000)

        #Turn Until Boom Reaches Tape
        while not on_tape(BOOM_TOPHAT):
                drive(500, -500)
        brake()

        #Lower Claw Into Drawer
        lower_arm()



if __name__ == "__main__":
        k.enable_servos()
        raise_arm()
        k.set_servo_position(BOOM_ARM, 1725)
        k.set_servo_position(JANNIS, 2047)
        k.set_servo_position(SWIPER, 0)

main()

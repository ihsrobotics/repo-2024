from config_loader import *
from ctypes import CDLL
kipr = "/usr/local/lib/libkipr.so"
k = CDLL(kipr)


def on_tape(sensor, black):
        return k.analog(sensor) > black

def drive(left_speed, right_speed, ms=0):
        k.mav(LEFT_WHEEL, left_speed)
        k.mav(RIGHT_WHEEL, right_speed)
        k.msleep(ms)
def brake():
        drive(0,0,1)
def stop_motor(port):
        k.mav(port, 0)
        k.msleep(1)
def turn_90(direction):
        if direction == 'RIGHT':
                drive(800, -800)
                k.msleep(1300)
        if direction == 'LEFT':
                drive(-800, 800)
                k.msleep(1300)

        
# the side of the tape the tophat follows
def line_follow(slow, fast, side, tophat=FRONT_TOPHAT, black=FRONT_BLACK):
        k.analog(tophat)
        if side.upper() == "RIGHT":
                 if not on_tape(tophat, black):
                        drive(slow, fast)
#                        print(f'tophat seeing {k.analog(tophat)}, turning left')
                 if on_tape(tophat, black):
                        drive(fast, slow)
#                        print(f'tophat seeing {k.analog(tophat)}, turning right')

        if side.upper() == "LEFT":
                if not on_tape(tophat, black):
                        drive(fast, slow)
  #                      print(f'tophat seeing {k.analog(tophat)}, turning right')
                if on_tape(tophat, black):
                        drive(slow, fast)
 #                       print(f'tophat seeing {k.analog(tophat)}, turning left')

def button_align():
        while k.digital(LEFT_BUTTON) != 1 or k.digital(RIGHT_BUTTON) != 1:
                if k.digital(LEFT_BUTTON) != 1:
                        k.mav(LEFT_WHEEL, 1500)
                        print('left!')
                else:
                        k.mav(RIGHT_WHEEL,0)
                if k.digital(RIGHT_BUTTON) != 1:
                        k.mav(RIGHT_WHEEL, 1500)
                        print('right!')
                else:
                        k.mav(RIGHT_WHEEL,0)



# def set_arm_pos(pos):
#         #if we are greater than end pos, RAISE arm
#         if k.analog(SLIDE) > pos:
#                 while k.analog(SLIDE) > pos:
#                         #if we are within 100 of the end pos, move arm SLOW
#                         if k.analog(SLIDE) - pos > 80:
#                                 k.mav(ARM, -750)
#                         else:
#                                 k.mav(ARM,-15)
#                         print(k.analog(SLIDE))
#         #if we are less than end pos, LOWER arm
#         else:
#                 while k.analog(SLIDE) < pos:
#                         #if we are within 100 of the end pos, move arm SLOW
#                         if pos - k.analog(SLIDE) > 30:
#                                 k.mav(ARM, 750)
#                         else:
#                                 k.mav(ARM,15)
#                         print(k.analog(SLIDE))

# #500 speed, 50 and 250 buffer

#         k.mav(ARM,0)

def set_arm_pos(pos):
        print(k.analog(SLIDE))
        if abs(k.analog(SLIDE) - pos) <= 20:
                pass
        #if we are greater than end pos, RAISE arm/ADD to slide
        elif k.analog(SLIDE) < pos:
                while k.analog(SLIDE) < pos:
                        #if we are within 100 of the end pos, move arm SLOW
                        if abs(k.analog(SLIDE) - pos) > 100:
                                k.mav(ARM, -750)
                        else:
                                k.mav(ARM,-100)
                        print(k.analog(SLIDE))
        #if we are less than end pos, LOWER arm/SUBTRACT from slide
        elif k.analog(SLIDE) > pos:
                while k.analog(SLIDE) > pos:
                        #if we are within 100 of the end pos, move arm SLOW
                        if abs(pos - k.analog(SLIDE)) > 100:
                                k.mav(ARM, 750)
                        else:
                                k.mav(ARM,100)
                        print(k.analog(SLIDE))
        k.mav(ARM,0)

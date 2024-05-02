import json

configs = {}

def load_configs():
    global configs
    with open('/home/pi/Documents/IME_files/start_seq/include/config.json') as f:
        configs = json.load(f)

load_configs()


LEFT_WHEEL = configs["LEFT_WHEEL"]
RIGHT_WHEEL = configs["RIGHT_WHEEL"]
ARM = configs["ARM"]

SWITCH = configs["SWITCH"]
LEFT_BUTTON = configs["LEFT_BUTTON"]
RIGHT_BUTTON = configs["RIGHT_BUTTON"]

FRONT_TOPHAT = configs["FRONT_TOPHAT"]
BOOM_TOPHAT = configs["BOOM_TOPHAT"]
SLIDE = configs["SLIDE"]

CLAW_SERVO = configs["CLAW_SERVO"]
BOOM_SERVO = configs["BOOM_SERVO"]
JANNIS_SERVO = configs["JANNIS_SERVO"]

FRONT_BLACK = configs["FRONT_BLACK"]
BOOM_BLACK = configs["BOOM_BLACK"]

BOOM_RIGHT_POS = configs["BOOM_RIGHT_POS"]
BOOM_LEFT_POS = configs["BOOM_LEFT_POS"]
BOOM_ASTRO_PICKUP_POS = configs["BOOM_ASTRO_PICKUP_POS"]

CLAW_COMB_CLOSE_POS = configs["CLAW_COMB_CLOSE_POS"]

ARM_UP_POS = configs["ARM_UP_POS"]
ARM_DOWN_POS = configs["ARM_DOWN_POS"] # unused

JANNIS_DOWN_POS = configs["JANNIS_DOWN_POS"]
JANNIS_UP_POS = configs["JANNIS_UP_POS"]

import os
import time
import pickle
import logging
import signal
import RPi.GPIO as GPIO

from datetime import datetime
from subprocess import Popen, PIPE, STDOUT, TimeoutExpired
from support_functions import sort_arr_time_2d

if os.path.exists("std.log"):
    os.remove("std.log")
# create logger object
logging.basicConfig(
    filename="std.log",
    filemode="a",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger()
logger.info("Starting Log File")

""" INITILIZATION """
diff_array = []
diff_arr_time_curr = 0
diff_arr_time_prev = 0
counter = 0
loop_counter = 0

MINUTES_IN_DAY = 1440
ALARM_PLAYTIME = 3
ALARM_TO_PLAY = "./alarm_sounds/generic_alarm.mp3"

global STAY_IN_LOOP
STAY_IN_LOOP = True

# GPIO Initialization
def alarm_stop_callback(channel):
    global STAY_IN_LOOP
    STAY_IN_LOOP = False


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(10, GPIO.RISING, callback=alarm_stop_callback)

logger.debug("Intiliazed Variables and GPIO")
logger.debug("Waiting for listfile.data to be ready")

""" LISTFILE.DATA INTILIZATION"""
while not os.path.exists("listfile.data"):
    time.sleep(1)
if os.path.isfile("listfile.data"):
    pass
else:
    raise ValueError("listfile.data isn't a file!")

logger.debug("listfile.data is ready, starting loop")

""" MAIN LOOP """
while True:
    loop_counter = loop_counter + 1

    while True:
        with open("listfile.data", "rb") as alarms:
            diff_array, diff_arr_time_curr = pickle.load(alarms)
        logger.debug("Diff Array Has Been Read")
        if diff_array != []:
            break
        time.sleep(1)

    if diff_array is not None or not diff_array == []:
        # update array if necessary to reset counter
        if diff_arr_time_curr != diff_arr_time_prev:
            diff_arr_time_prev = diff_arr_time_curr
            counter = 0
            logger.debug("Array Updated")
        elif diff_arr_time_curr == diff_arr_time_prev:
            # reset counter if it has reached the max array len and it hasnt been updated
            if counter == len(diff_array):
                counter = 0
                logger.debug("counter updated")
            logger.debug("Array Not Updated")

        # iterate by counter and check if the time matches then play sound if so for ALARM_PLAYTIME seconds
        if counter < len(diff_array):
            alarm_time = diff_array[counter][1]
            d = datetime.now()
            curr_time = d.strftime("%H:%M")

            logger.info("Time Being Checked: " + alarm_time)
            if alarm_time == curr_time:
                counter = counter + 1
                diff_array = sort_arr_time_2d(diff_array)

                while STAY_IN_LOOP:  # Repeat audio until button has been pressed
                    proc = Popen(["mpg123", ALARM_TO_PLAY])
                    try:
                        outs, errs = proc.communicate(timeout=ALARM_PLAYTIME)
                    except TimeoutExpired:
                        proc.kill()
                        outs, errs = proc.communicate()
                    logger.critical("** ALARM **")
                logger.critical("** ALARM DONE **")

                STAY_IN_LOOP = True  # Reset loop variable for next alarm
            else:
                pass
                logger.debug("It Is Not Time")
    else:
        logger.warning("diff_array is None")

    logger.debug(f"Loop End: {loop_counter}")
    time.sleep(3)

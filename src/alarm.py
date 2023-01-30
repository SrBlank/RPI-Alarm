import os
import time
import pickle
import logging
import signal

from datetime import datetime
from subprocess import Popen, PIPE, STDOUT, TimeoutExpired, check_output, CalledProcessError

from support_functions import sort_arr_time
from alarm_class import Alarm

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
ALARM_PLAYTIME = 5
ALARM_TO_PLAY = "./alarm_sounds/generic_alarm.mp3"
ENABLE_BUTTON = True
GPIO_INPUT_PIN = 10

global STAY_IN_LOOP
STAY_IN_LOOP = True

# GPIO Initialization
def alarm_stop_callback(channel):
    logger.info("Button Pressed")

    global STAY_IN_LOOP
    STAY_IN_LOOP = False

    try: 
        process_id = int(check_output(["pidof","-s","mpg123"]))
        os.system("kill -9 " + str(process_id))
        logger.info("Process SKilled Sucessfully")
    except CalledProcessError:
        print("Process Does Not Exist")

if ENABLE_BUTTON:
    import RPi.GPIO as GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(GPIO_INPUT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(GPIO_INPUT_PIN, GPIO.RISING, callback=alarm_stop_callback)
    logger.info("Intiliazed Variables and GPIO")
else:
    logger.info("Intilizaed Variables, button is disabled")

logger.info("Waiting for listfile.data to be ready")

""" LISTFILE.DATA INTILIZATION"""
while not os.path.exists("listfile.data"):
    time.sleep(1)
if os.path.isfile("listfile.data"):
    pass
else:
    raise ValueError("listfile.data isn't a file!")

logger.info("listfile.data is ready, starting loop")

def playAlarm(alarm_instance):
    proc = Popen(["mpg123", alarm_instance.alarm_sound])
    try:
        outs, errs = proc.communicate(timeout=int(alarm_instance.playtime))
    except TimeoutExpired:
        proc.kill()
        outs, errs = proc.communicate()
    logger.critical("** ALARM **")

""" MAIN LOOP """
while True:
    loop_counter = loop_counter + 1

    while True:
        logger.debug("finding diff_array")
        with open("listfile.data", "rb") as alarms:
            diff_array, diff_arr_time_curr = pickle.load(alarms)
        logger.debug("Diff Array Has Been Read")
        if diff_array != [] and diff_array is not None:
            logger.debug("found diff_array")
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
                d = datetime.now()
                curr_time = d.strftime("%H:%M")
                if diff_array[0].time == curr_time:
                    logger.debug("sleeping")
                    time.sleep(60)
                counter = 0
                logger.debug("counter updated")
            logger.debug("Array Not Updated")

        # iterate by counter and check if the time matches then play sound if so for ALARM_PLAYTIME seconds
        if counter < len(diff_array):
            STAY_IN_LOOP = True  # Reset loop variable for next alarm 
            alarm_instance = diff_array[counter]
            alarm_time = diff_array[counter].time #[1]
            d = datetime.now()
            curr_time = d.strftime("%H:%M")

            logger.info("Time Being Checked: " + alarm_instance.time)
            if alarm_instance.time == curr_time:
                counter = counter + 1
                diff_array = sort_arr_time(diff_array)

                if alarm_instance.button and ENABLE_BUTTON:
                    logger.critical("** ALARM DONE WITH BUTTON **")
                    while STAY_IN_LOOP:  # Repeat audio until button has been pressed
                        playAlarm(alarm_instance) 
                else:
                    logger.critical("** ALARM DONE NO BUTTON **")
                    playAlarm(alarm_instance)

            else:
                pass
                logger.debug("It Is Not Time")
    else:
        logger.warning("diff_array is None")

    logger.debug(f"Loop End: {loop_counter}")
    time.sleep(3)
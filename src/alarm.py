import os
import time
import pickle
import logging
import signal
import pygame
import keyboard

from datetime import datetime
from subprocess import (
    Popen,
    PIPE,
    STDOUT,
    TimeoutExpired,
    check_output,
    CalledProcessError,
)

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
pygame.init() # move this at a later time

diff_array = []
diff_arr_time_curr = 0
diff_arr_time_prev = 0
counter = 0
loop_counter = 0

MINUTES_IN_DAY = 1440
ALARM_PLAYTIME = 5
ALARM_TO_PLAY = "./alarm_sounds/generic_alarm.mp3"
GPIO_INPUT_PIN = 10


"""
Alarm Control Functions
"""
#
# Function will handle intterupt from GPIO or keyboard
#
def interrupt_handler(channel=None):
    logger.critical("Interrupt Detected")
    pygame.mixer.music.stop()

#
# Function will play alarm for x time or loop until intterupt
#
def play_alarm_timer(alarm_instance):
    pygame.mixer.music.load(alarm_instance.alarm_sound)
    pygame.mixer.music.play(loops=-1)
    if(alarm_instance.input == "Timer"):
        time.sleep(int(alarm_instance.playtime))
        pygame.mixer.music.stop()

"""
Button input intialization
"""
try:
    logger.info("Attempting to intialize GPIO")
    import RPi.GPIO as GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(GPIO_INPUT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(GPIO_INPUT_PIN, GPIO.RISING, callback=interrupt_handler)
    logger.info("Intiliazed Variables and GPIO")
except (RuntimeError, ModuleNotFoundError):
    logger.info("Failed to intialize GPIO, keyboard input will be used")
    keyboard.add_hotkey("esc", interrupt_handler)
    logger.info("Intilizaed Variables and Keyboard")


""" 
LISTFILE.DATA INTILIZATION
"""
logger.info("Waiting for listfile.data to be ready")
while not os.path.exists("listfile.data"):
    time.sleep(1)
if os.path.isfile("listfile.data"):
    pass
else:
    raise ValueError("listfile.data isn't a file!")


""" 
MAIN LOOP 
"""
logger.info("listfile.data is ready, starting loop")
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
            alarm_instance = diff_array[counter]
            alarm_time = diff_array[counter].time  # [1]
            d = datetime.now()
            curr_time = d.strftime("%H:%M")

            logger.info("Time Being Checked: " + alarm_instance.time)
            if alarm_instance.time == curr_time:
                counter = counter + 1
                diff_array = sort_arr_time(diff_array)

                logger.critical("** ALARM DONE -- INPUT TYPE -- " + (alarm_instance.input).upper() + " **")
                if(alarm_instance.input == "Sensor"):
                    # TODO
                    pass
                elif alarm_instance.input == "Button" or alarm_instance.input == "Timer":
                    play_alarm_timer(alarm_instance)          

            else:
                pass
                logger.debug("It Is Not Time")
    else:
        logger.warning("diff_array is None")

    logger.debug(f"Loop End: {loop_counter}")
    time.sleep(3)

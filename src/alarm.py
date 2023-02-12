import os
import time
import pickle
import logging
import pygame
import requests
import json
KEYBOARD_INIT = True
try:
    import pynput
except:
    KEYBOARD_INIT = False
    print("UNABLE TO IMPORT PYNPUT")

from datetime import datetime

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
pygame.init()

diff_array = []
diff_arr_time_curr = 0
diff_arr_time_prev = 0
counter = 0
loop_counter = 0
sensor_time_curr = 0
sensor_time_prev = 0

SENSOR_TIME_THRESHOLD = 10
PROXIMITY = 20 # inches
MINUTES_IN_DAY = 1440
ALARM_PLAYTIME = 5
ALARM_TO_PLAY = "./alarm_sounds/generic_alarm.mp3"
GPIO_INPUT_PIN = 10

"""
Alarm Control Functions
"""
#
# Function will get data from /detect
# 
def check_distance_data():
    response = requests.get("http://10.0.0.23:5000/detect")
    data = json.loads(response.text)
    distance = data["distance"]

    time = data["time"]
    h, m, s = time.split(':')
    sensor_time_prev = int(h) * 3600 + int(m) * 60 + int(s)
    d = datetime.now()
    rn = d.strftime("%H:%M:%S")
    hO, mO, sO = rn.split(":")
    sensor_time_curr = int(hO) * 3600 + int(mO) * 60 + int(sO)

    if sensor_time_curr - sensor_time_prev <= SENSOR_TIME_THRESHOLD: # if the data is less than 2 minutes old
        return data["distance"]  
    else:
        return 10000          

#
# Function will handle intterupt from GPIO or keyboard
#
def interrupt_handler_keyboard(channel=None):
    if KEYBOARD_INIT and channel == pynput.keyboard.Key.esc:
        pygame.mixer.music.stop()
        logger.critical("Interrupt Detected - Alarm Stopped - Interrupt Type - Keyboard")


def interrupt_handler_GPIO(channel=None):
    pygame.mixer.music.stop()
    logger.critical("Interrupt Detected - Alarm Stopped - Interrupt Type - GPIO")



#
# Function will handle how alarm is played with the sensor data
#
def play_alarm_sensor(alarm_instance):
    pygame.mixer.music.load(alarm_instance.alarm_sound)
    pygame.mixer.music.play(loops=-1)
    distance = 0
    while True:
        logger.debug("Distance - " + str(distance))
        distance = check_distance_data()
        if(distance < PROXIMITY):
            break
    pygame.mixer.music.stop()
    logger.info("Proximity Breached - Alarm Stopped - Distance - " + str(distance))
#
# Function will play alarm for x time or loop until intterupt
#
def play_alarm_timer(alarm_instance):
    pygame.mixer.music.load(alarm_instance.alarm_sound)
    pygame.mixer.music.play(loops=-1)
    if(alarm_instance.input == "Timer"):
        time.sleep(int(alarm_instance.playtime))
        pygame.mixer.music.stop()
        logger.critical("Timer Finished - Alarm Stopped")

"""
Button input intialization
"""
if KEYBOARD_INIT:
    listener = pynput.keyboard.Listener(on_press=interrupt_handler_keyboard) 
    listener.start()
    logger.info("Intilizaed Keyboard Interrupt")
else:
    logger.info("Unable to Initalize Keyboard Interrupt")

try:
    import RPi.GPIO as GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(GPIO_INPUT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(GPIO_INPUT_PIN, GPIO.RISING, callback=interrupt_handler_GPIO)
    logger.info("Intiliazed Variables and GPIO")
except:
    pass
#except (RuntimeError, ModuleNotFoundError, ImportError):
    logger.info("Failed to intialize GPIO")

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

                logger.critical("Playing Alarm - Input Type - " + (alarm_instance.input).upper())
                if(alarm_instance.input == "Sensor"):
                    play_alarm_sensor(alarm_instance)
                elif alarm_instance.input == "Button" or alarm_instance.input == "Timer":
                    play_alarm_timer(alarm_instance)          

            else:
                pass
                logger.debug("It Is Not Time")
    else:
        logger.warning("diff_array is None")

    logger.debug(f"Loop End: {loop_counter}")
    time.sleep(3)

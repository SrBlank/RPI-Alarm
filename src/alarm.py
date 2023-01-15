import os
import time
import pickle
import logging
import signal
import RPi.GPIO as GPIO

from datetime import datetime
from subprocess import Popen, PIPE, STDOUT, TimeoutExpired
from support_functions import sort_arr_time_2d

# Configuration
ALARM_PLAYTIME = 3
ALARM_TO_PLAY = './alarm_sounds/generic_alarm.mp3'

temp_array = []
rn = 0
rn_old = 0
counter = 0
loop_counter = 0
MINUTES_IN_DAY = 1440

global STAY_IN_LOOP; STAY_IN_LOOP = True

# GPIO Initialization
def alarm_stop_callback(channel):
    global STAY_IN_LOOP; STAY_IN_LOOP = False

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(10,GPIO.RISING,callback=alarm_stop_callback)

# waits until listfile.data is created by web_server
while not os.path.exists("listfile.data"):
    time.sleep(1)
# validates listfile.data
if os.path.isfile("listfile.data"):
    pass
else:
    raise ValueError("listfile.data isn't a file!")

# removes old log if one exists
if os.path.exists("std.log"):
    os.remove("std.log")
# creates logger object
logging.basicConfig(filename='std.log', filemode='a', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.info("Starting Log File")

# first time diff_array load - may not need
with open('listfile.data', 'rb') as alarms:
    diff_array, rn  = pickle.load(alarms)
for i in diff_array:
    temp_array.append(i)


while True: 
    loop_counter = loop_counter + 1

    # read from data file 
    logger.debug(f'Loop Start: {loop_counter}')
    with open('listfile.data', 'rb') as alarms:
        diff_array, rn = pickle.load(alarms)
        logger.debug("Diff Array Has Been Read")
    
    # sort array
    if diff_array != None:
        diff_array = sort_arr_time_2d(diff_array)
        logger.debug("Array Resorted")

    if diff_array != None:
        # update array if necessary to reset counter
        # compare time the file is loaded to the previous time it was loaded
        if rn != rn_old:
            rn_old = rn
            # copy temp array
            temp_array.clear()
            for i in range(0, len(diff_array)):
                temp_array.append(diff_array[i])
            # reset counter b/c new array
            counter = 0
            logger.debug("Array Updated")
        elif rn == rn_old:
            # reset counter if it has reached the max array len and it hasnt been updated
            if(counter == len(temp_array)):
                counter = 0
                logger.debug("counter updated")
            logger.debug("Array Not Updated")
            pass
        
        # iterate by counter and check if the time matches then play sound if so for ALARM_PLAYTIME seconds
        if counter < len(temp_array):
            # grab first time from temp_array
            alarm_time = temp_array[counter][1]
            # grab current time
            d = datetime.now()
            curr_time = d.strftime("%H:%M")

            logger.info("Time Being Checked: " + alarm_time)
            # check if it is time
            if alarm_time == curr_time:
                counter = counter + 1
                logger.critical("**ALARM DONE**")
                # Repeat audio until button has been pressed
                while STAY_IN_LOOP:
                    proc = Popen(['mpg123', ALARM_TO_PLAY])
                    try:
                        outs, errs = proc.communicate(timeout=ALARM_PLAYTIME)
                    except TimeoutExpired:
                        proc.kill()
                        outs,errs = proc.communicate()
                    logger.critical("**ALARM PLAYED**")
                logger.critical("**BUTTON PRESSED**")
                
                # Reset loop variable for next alarm
                STAY_IN_LOOP = True 
            else:
                pass
                logger.debug("It Is Not Time")
    else:
        logger.warning("diff_array is None")
        
    logger.debug(f"Loop End: {loop_counter}")
    time.sleep(3)



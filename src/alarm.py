import os
import time
import pickle
import logging

from datetime import datetime
from subprocess import Popen, PIPE, STDOUT, TimeoutExpired

from support_functions import sort_arr_time_2d

temp_array = []
rn = 0
rn_old = 0
counter = 0
loop_counter = 0
MINUTES_IN_DAY = 1440

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
logging.basicConfig(filename='std.log', filemode='a', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
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
        if rn != rn_old:
            logger.debug("Array Updated")
            rn_old = rn
            temp_array.clear()
            for i in range(0, len(diff_array)):
                temp_array.append(diff_array[i])
            counter = 0
        elif rn == rn_old:
            logger.debug("Array Not Updated")
            pass

        if counter < len(temp_array):
            alarm_time = temp_array[counter][1]
            d = datetime.now()
            curr_time = d.strftime("%H:%M")
            logger.info("Time Being Checked: " + alarm_time)
            if alarm_time == curr_time:
                counter = counter + 1
                logger.critical("**ALARM DONE**")
                proc = Popen(['gedit', 'file.txt'])
                try:
                    outs, errs = proc.communicate(timeout=10)
                except TimeoutExpired:
                    proc.kill()
                    outs,errs = proc.communicate()
            else:
                pass
                logger.debug("It Is Not Time")
    else:
        logger.warning("diff_array is None")
        
    logger.debug(f"Loop End: {loop_counter}")
    time.sleep(3)



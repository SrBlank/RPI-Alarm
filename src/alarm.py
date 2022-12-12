import pickle
import time
from datetime import datetime
import os
from subprocess import Popen, PIPE, STDOUT
import logging

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
logging.basicConfig(filename='std.log', filemode='a', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# first time diff_array load - may not need
with open('listfile.data', 'rb') as alarms:
    diff_array, rn  = pickle.load(alarms)
for i in diff_array:
    temp_array.append(i)

def sort_arr_time(D2_array_to_sort=[]):
    sorted_array = []
    if len(D2_array_to_sort) != 0:
        temp_array = []
        for i in range(0, len(D2_array_to_sort)):
            temp_array.append(D2_array_to_sort[i][1])

        d = datetime.now()
        formatted_d = d.strftime("%H:%M")
        hoursC = d.strftime("%H")
        minutesC = d.strftime("%M")
        conver_min = int(hoursC)*60 + int(minutesC)

        for i in range(0, len(temp_array)):
            hours_current = temp_array[i][0] + temp_array[i][1]
            minutes_current = temp_array[i][3] + temp_array[i][4]
            conver_current = int(hours_current)*60 + int(minutes_current)

            difference = conver_current - conver_min
            if (difference > 0):
                index_b_time = [difference, hours_current + ":" + minutes_current]
                sorted_array.append(index_b_time)
            elif (difference <= 0):
                index_b_time = [MINUTES_IN_DAY-(difference*-1), hours_current + ":" + minutes_current]
                sorted_array.append(index_b_time)
        sorted_array.sort(key=lambda x: x[0])
        return sorted_array 
    else:
        pass

while True: 
    loop_counter = loop_counter + 1
        
    logger.debug(f'Loop Start: {loop_counter}')
    with open('listfile.data', 'rb') as alarms:
        diff_array, rn = pickle.load(alarms)
        logger.debug("Diff Array Has Been Read")

    diff_array = sort_arr_time(diff_array)
    logger.debug("Array Resorted")

    if rn != rn_old:
        logger.info("Array Updated")
        rn_old = rn
        temp_array.clear()
        for i in range(0, len(diff_array)):
            temp_array.append(diff_array[i])
        counter = 0
    elif rn == rn_old:
        logger.info("Array Not Updated")
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
            proc.wait()
        else:
            pass
            logger.debug("It Is Not Time")
        
    logger.debug(f"Loop End: {loop_counter}")
    time.sleep(3)



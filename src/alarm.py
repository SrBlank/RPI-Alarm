######
# BUG: List needs to be resortted 
# BUG: List needs to be updated after removing alarms
# BUG: Log file is not appending data - CURRENT 
######

import pickle
import time
from datetime import datetime
import os
from web_server import sort_arr_time
from subprocess import Popen, PIPE, STDOUT
import logging
temp_array = []
rn = 0
rn_old = 0
counter = 0
loop_counter = 0


while not os.path.exists("listfile.data"):
    time.sleep(1)

if os.path.isfile("listfile.data"):
    pass
else:
    raise ValueError("listfile.data isn't a file!")

if os.path.exists("std.log"):
    os.remove("std.log")
logging.basicConfig(filename='std.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()



with open('listfile.data', 'rb') as alarms:
    diff_array, rn  = pickle.load(alarms)
for i in diff_array:
    temp_array.append(i)

#fout = open("log.txt", "a")
while True:
    # FIX THIS
    # with open("./log.txt", 'r') as fp:
    #     x = len(fp.readlines())
    #     if(x >= 140):
    #         #with open("sample3.txt", "r") as fp:
    #         fp.truncate()

    
    loop_counter = loop_counter + 1
    d = datetime.now()
    curr_time = d.strftime("%H:%M:%S")
        
    logger.debug(f'Loop Start: {loop_counter}')
    with open('listfile.data', 'rb') as alarms:
        diff_array, rn = pickle.load(alarms)
        logger.debug("Diff Array Has Been Read")

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
            # temp_array = sort_arr_time()
            logger.critical("**ALARM DONE**")
            proc = Popen(['gedit', 'file.txt'])
            proc.wait()
        else:
            pass
            logger.debug("It Is Not Time")
        
    logger.debug(f"Loop End: {loop_counter}")
    #print(temp_array)
    time.sleep(3)



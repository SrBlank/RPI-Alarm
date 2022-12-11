#from subprocess import Popen, PIPE, STDOUT

#p = Popen([sys.executable, '-u', './UbLstm.py', '-p', '/home/hipe/Documents/output.wav'], stdout = PIPE, stderr=STDOUT, bufsize=1)

import pickle
import time
from datetime import datetime
temp_array = []
rn = 0
rn_old = 0
counter = 0

with open('listfile.data', 'rb') as alarms:
    diff_array, rn  = pickle.load(alarms)
for i in diff_array:
    temp_array.append(i)

while True:
    with open('listfile.data', 'rb') as alarms:
        diff_array, rn = pickle.load(alarms)

    if rn != rn_old:
        rn_old = rn
        temp_array.clear()
        for i in range(0, len(diff_array)):
            temp_array.append(diff_array[i])
        counter = 0
    elif rn == rn_old:
        pass

    if counter < len(temp_array):
        alarm_time = temp_array[counter][1]
        d = datetime.now()
        curr_time = d.strftime("%H:%M")
        if alarm_time == curr_time:
            counter = counter + 1
            print("ALARM DONE") 
        

    print(temp_array)
    time.sleep(3)




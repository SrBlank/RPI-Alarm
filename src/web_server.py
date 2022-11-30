from flask import Flask, render_template, redirect, url_for, request, flash
from dotenv import load_dotenv, find_dotenv
import os

from datetime import datetime

from threading import Thread
import schedule
import time
from subprocess import Popen, PIPE, STDOUT

load_dotenv(find_dotenv())

app = Flask(__name__)
app.secret_key = os.getenv('app_secret')

list_of_alarms = ['18:45', '01:00', '10:15', '01:20', '00:01', '21:39']
alarms_selected = [] # ['18:45', '01:00', '10:15', '01:20', '00:01', '22:40', '22:39']
diff_array = []
RUNNING = True


MINUTES_IN_DAY = 1440

"""
HTML PAGE RENDERING
"""

@app.route("/")
def hello_world():
    """
    RUNNING = False
    if len(alarms_selected) != 0:
        sort_arr_time(alarms_selected)
        if thread.is_alive():
            thread.join()
            print("STOPPED THREAD")
        RUNNING = True
        thread.start()
        print("STARTED THREAD")
    """
 
    return render_template(
        "index.html",
        alarms_list = list_of_alarms,
        alarms_selcted = alarms_selected
        )

#
# Function renders remove_alarm.html
#
@app.route("/removeablealarms", methods=['POST'])
def removeablealarms():
    return render_template(
        "remove_alarm.html",
        alarms_list = list_of_alarms
        )

"""
FORM PROCESSES
"""

#
# Function will remove alarms from list
#
@app.route("/remove_alarms", methods=["POST"])
def remove_alarms():
    form_data = request.form
    form_checked = request.form.getlist("checkbox")
    #print(form_data)
    for i in form_checked:
        list_of_alarms.remove(i)   
        
    return redirect(url_for("hello_world"))

#
# function will check/uncheck alarm boxes
#
@app.route("/update_alarms", methods=['POST'])
def update_alarms():
    form_data = request.form
    form_checked = request.form.getlist("checkbox")
    form_checkedN = request.form.getlist("checkboxN")
    alarms_selected.clear()

    for j in form_checkedN:
        alarms_selected.append(j)
    for k in form_checked:
        alarms_selected.append(k)

    sort_list(alarms_selected)
    
    return redirect(url_for("hello_world"))

#
# Function will add a new time to the list
#
@app.route("/process_time", methods = ['POST'])
def process_time():
    form_data = request.form

    for i in list_of_alarms:
        if i == form_data['time_box']:
            flash('duplicate')
            return redirect(url_for("hello_world"))

    list_of_alarms.append(form_data['time_box'])
    sort_list(list_of_alarms)
    
    return redirect(url_for("hello_world"))

"""
SUPPORTING FUNCTIONS
"""

#
# Function will sort the array from the earliest to latest time 
#
def sort_arr_time(array):    

    d = datetime.now()
    formatted_d = d.strftime("%H:%M")
    hoursC = d.strftime("%H")
    minutesC = d.strftime("%M")
    conver_min = int(hoursC)*60 + int(minutesC)

    for i in range(0, len(array)):
        hours_current = array[i][0] + array[i][1]
        minutes_current = array[i][3] + array[i][4]
        conver_current = int(hours_current)*60 + int(minutes_current)

        difference = conver_current - conver_min
        if(difference > 0):
            index_b_time = [difference, hours_current + ":" + minutes_current]
            diff_array.append(index_b_time)
        elif (difference <= 0):
            index_b_time = [MINUTES_IN_DAY-(difference*-1), hours_current + ":" + minutes_current]
            diff_array.append(index_b_time)

    diff_array.sort(key=lambda x: x[0])
    #print(diff_array) 

def sort_list(sort_array):
    for i in range(1,len(sort_array)):
        for j in range(0, len(sort_array)-1):
            hours_current = sort_array[j][0] + sort_array[j][1]
            minutes_current = sort_array[j][3] + sort_array[j][4]
            hours_next = sort_array[j+1][0] + sort_array[j+1][1]
            minutes_next = sort_array[j][3] + sort_array[j][4]

            if int(hours_current) >= int(hours_next) :
                if int(minutes_current) <= int(minutes_next):
                    temp = hours_current + ':' + minutes_current
                    sort_array[j] = sort_array[j+1]
                    sort_array[j+1] = temp
def checkTime():
    while RUNNING:
        print("function call")
        if len(diff_array) != 0:
            run_alarm()
            diff_array.pop(0)
            print(diff_array)
        time.sleep(.1)
    """
    print("STARTING")
    time.sleep(1)
    if len(diff_array) != 0:
        for i in range(0, len(diff_array)):
            run_alarm()
            #alarms_selected.remove(diff_array[0][1])
            diff_array.pop(0)
    """

def run_alarm():
    current_alarm = diff_array[0][1]
    now = (datetime.now()).strftime("%H:%M")
    #print(now)
    while now != current_alarm and RUNNING:
        now = (datetime.now()).strftime("%H:%M")
        time.sleep(1)

    if RUNNING:
        print("ALARM " + str(current_alarm))
 

thread = Thread(target = checkTime, daemon=True)
#thread.start()

if __name__=="__main__":
    #int_array = [5,1,3,4]
    #sort_arr_time(alarms_selected)
    #schedule.every(1).second.do(start_alarm)
    #stop_run_continuously = run_continuously()
    #thread.setDaemon(True)
    alarms_selected = [1,2,3]
    time.sleep(1)
    alarms_selected = [1,2]
    time.sleep(1)
    alarms_selected = [1]
    #app.run()
    #thread.join()
    #stop_run_continuously.set()


"""
def run_continuously(interval=1):
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run

def start_alarm():
    p = Popen(['python3', '-u', './alarm.py'], stdout = PIPE, stderr=STDOUT, bufsize=1)
    return schedule.CancelJob
"""
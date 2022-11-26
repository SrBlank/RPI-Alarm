from flask import Flask, render_template, redirect, url_for, request, flash
from dotenv import load_dotenv, find_dotenv
import os

from datetime import datetime

import threading
import schedule
import time
from subprocess import Popen, PIPE, STDOUT

load_dotenv(find_dotenv())

app = Flask(__name__)
app.secret_key = os.getenv('app_secret')

list_of_alarms = ['18:45', '01:00', '10:15', '01:20']
alarms_selected = ['18:45', '01:00', '10:15', '01:20']

def sort_arr_time(array):    

    d = datetime.now()
    formatted_d = d.strftime("%H:%M")
    hoursC = d.strftime("%H")
    minutesC = d.strftime("%M")
    """
    newList = []
    for i in range(1,len(array)):
        hours_current = array[j][0] + array[j][1]
        minutes_current = array[j][3] + array[j][4]
        if int(hours_current) == int(hoursC):
            for j in array:
                if int(j[0:2]) == hoursC:
                    newList.append(j)
    """
    for i in range(1,len(array)):
        for j in range(0, len(array)-1):
            hours_current = array[j][0] + array[j][1]
            minutes_current = array[j][3] + array[j][4]
            hours_next = array[j+1][0] + array[j+1][1]
            minutes_next = array[j+1][3] + array[j+1][4]

            if int(hoursC) <= int(hours_current):
                print('outehere')
                #if int(minutesC) >= int(minutes_next):
                print('here')
                temp = hours_current + ':' + minutes_current
                array[j] = array[j+1]
                array[j+1] = temp
            
            """
            if int(hours_current) >= int(hours_next) :
                if int(minutes_current) <= int(minutes_next):
                    temp = hours_current + ':' + minutes_current
                    array[j] = array[j+1]
                    array[j+1] = temp
            """


    print(array)

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

"""
HTML PAGE RENDERING
"""

@app.route("/")
def hello_world():
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
    print(form_data)
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
    
if __name__=="__main__":
    sort_arr_time(alarms_selected)
    #schedule.every(1).second.do(start_alarm)
    #stop_run_continuously = run_continuously()
    #app.run()
    #stop_run_continuously.set()

 
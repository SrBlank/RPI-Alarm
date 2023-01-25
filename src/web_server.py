import os
import sys
import pickle

from datetime import datetime
from subprocess import Popen, PIPE, STDOUT
from dotenv import load_dotenv, find_dotenv
from flask import Flask, render_template, redirect, url_for, request, flash

from support_functions import sort_arr_time, sort_list
from alarm_class import Alarm

load_dotenv(find_dotenv())
app = Flask(__name__)
app.secret_key = os.getenv('app_secret')

MINUTES_IN_DAY = 1440
ADD_2_ALARMS = True
DEL_LISTFILE = True

list_of_alarms = [] 
alarms_sel = [] 
alarms_sel_sorted_2d = []

#### THIS CODE WILL ADD 2 ALARMS #### 
if ADD_2_ALARMS:
    d = datetime.now()
    min_1 = str(int(d.strftime("%M"))+1)
    hours = d.strftime("%H")
    min_2 = str(int(d.strftime("%M"))+2)
    if len(min_1) == 1:
        now_1 = hours + ":0" + min_1 
        now_2 = hours + ":0" + min_2 
    else:
        now_1 = hours + ":" + min_1
        now_2 = hours + ":" + min_2 
    
    list_of_alarms.append(Alarm(now_1))
    list_of_alarms.append(Alarm(now_2))
    alarms_sel.append(Alarm(now_1))
    alarms_sel.append(Alarm(now_2))

"""
HTML PAGE RENDERING
"""
@app.route("/")
def hello_world():
    d = datetime.now()
    rn = d.strftime("%H:%M:%S")

    alarms_sel_sorted_2d = sort_arr_time(alarms_sel) 
    with open('listfile.data', 'wb') as alarms:
        pickle.dump([alarms_sel_sorted_2d, rn], alarms) 

    sort_arr_time(list_of_alarms) 
    alarms_sel_times = []
    for i in alarms_sel: 
        alarms_sel_times.append(i.time)

    return render_template(
        "index.html",
        alarms_list = list_of_alarms,
        alarms_selcted = alarms_sel_times 
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
    for i in list_of_alarms:
        if i.time in form_checked:
            list_of_alarms.remove(i)

    for i in alarms_sel:
        if i.time in form_checked:
            alarms_sel.remove(i)
        
    return redirect(url_for("hello_world"))

#
# function will check/uncheck alarm boxes
#
@app.route("/update_alarms", methods=['POST'])
def update_alarms():
    form_data = request.form
    form_checked = request.form.getlist("checkbox")
    form_checkedN = request.form.getlist("checkboxN")
    alarms_sel.clear() 
    
    for j in form_checkedN:
        alarms_sel.append(Alarm(j)) 
    for k in form_checked:
        alarms_sel.append(Alarm(k))

    flash('Alarms Updated!')
    return redirect(url_for("hello_world"))


#
# New function for getting new alarm form data
#

@app.route("/process_time", methods=['POST'])
def new_alarm():
    form_data = request.form
    
    new_time = form_data["time_prompt"]
    new_playback = form_data["playback_time"]

    if new_time in list_of_alarms:
        flash("Alarm Already Exists!")
        return redirect(url_for("hello_world"))
    if isinstance(new_playback, int):
        flash("Playback Must Be An Integer!")
        return redirect(url_for("hello_world"))
    if len(new_playback) == 0:
        list_of_alarms.append(Alarm(new_time)) 
    else:
        list_of_alarms.append(Alarm(new_time, new_playback))

    flash("Alarm " + new_time + " added!")
    return redirect(url_for("hello_world"))

if __name__=="__main__":
    if DEL_LISTFILE:
        if os.path.exists("listfile.data"):
            os.remove("listfile.data")
            print("removed listfile.data")
        else:
            print("listfile.data will be created")

        with open('listfile.data', 'wb') as alarms:
            pickle.dump([[], 0], alarms) 

    #p = Popen([sys.executable, '-u', './alarm.py'], stdout = PIPE, stderr=STDOUT, bufsize=1)
    app.run(host='0.0.0.0')

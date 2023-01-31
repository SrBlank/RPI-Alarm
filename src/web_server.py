import os
import sys
import pickle

from datetime import datetime, timedelta
from subprocess import Popen, PIPE, STDOUT
from dotenv import load_dotenv, find_dotenv
from flask import Flask, render_template, redirect, url_for, request, flash

from support_functions import sort_arr_time
from alarm_class import Alarm

load_dotenv(find_dotenv())
app = Flask(__name__)
app.secret_key = os.getenv('app_secret')

MINUTES_IN_DAY = 1440
ADD_2_ALARMS = False
DEL_LISTFILE = True
NAP_DEFAULT = 40 # To be changed into settings

list_of_alarms = [] 
alarms_sel = [] 
alarms_sel_sorted_2d = []

alarm_sounds = os.listdir("./alarm_sounds")

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
    
    list_of_alarms.append(Alarm(now_1, playtime=6))
    list_of_alarms.append(Alarm(now_2))
    alarms_sel.append(Alarm(now_1, playtime=6))
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
        alarms_selcted = alarms_sel_times,
        alarm_sounds = alarm_sounds
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

#
# Function renders settings.html
#
@app.route("/settings", methods=["POST"])
def settings():
    return render_template("settings.html")

"""
FORM PROCESSES
"""
#
# Function will process nap button 
#
@app.route("/timer_process", methods=["POST"])
def timer_process():
    curr_time = datetime.now()
    time_change = timedelta(minutes=NAP_DEFAULT)
    new_time = curr_time + time_change
    new_time = new_time.strftime("%H:%M")

    for item in list_of_alarms:
        if new_time in item:
            flash("Alarm Already Exists!")
            return redirect(url_for("hello_world"))

    add_alarm = Alarm(new_time)

    list_of_alarms.append(add_alarm)
    alarms_sel.append(add_alarm)

    return redirect(url_for("hello_world"))

#
# Function will update settings
#
@app.route("/update_settings", methods=["POST"])
def update_settings():
    form_data = request.form

    return redirect(url_for("hello_world"))

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
    
    for checked in form_checkedN:
        for alarm in list_of_alarms:
            if checked in alarm:
                alarms_sel.append(alarm)

    for unchecked in form_checked:
        for alarm in list_of_alarms:
            if unchecked in alarm:
                alarms_sel.append(alarm)

    flash('Alarms Updated!')
    return redirect(url_for("hello_world"))


#
# New function for getting new alarm form data
#
@app.route("/process_time", methods=['POST'])
def new_alarm():
    form_data = request.form
    #print(form_data)

    new_time = form_data["time_prompt"]
    new_playback = form_data["playback_time"]
    alarm_sounds_form = form_data["alarm_sound"]
    enable_button_form = form_data["enable_button"]
    if enable_button_form == "Enable":
        enable_button_bool = True
    else:
        enable_button_bool = False

    for item in list_of_alarms:
        if new_time in item:
            flash("Alarm Already Exists!")
            return redirect(url_for("hello_world"))
    if isinstance(new_playback, int):
        flash("Playback Must Be An Integer!")
        return redirect(url_for("hello_world"))

    add_alarm = Alarm(new_time,
                    playtime=new_playback,
                    alarm_sound=alarm_sounds_form,
                    enable_button=enable_button_bool
                    )
    list_of_alarms.append(add_alarm)

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

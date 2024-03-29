import os
import sys
import pickle
import json

from datetime import datetime, timedelta
from subprocess import Popen, PIPE, STDOUT
from dotenv import load_dotenv, find_dotenv
from flask import Flask, render_template, redirect, url_for, request, flash

from support_functions import sort_arr_time
from alarm_class import Alarm

load_dotenv(find_dotenv())
app = Flask(__name__)
app.secret_key = os.getenv("app_secret")

MINUTES_IN_DAY = 1440
ADD_2_ALARMS = False
DEL_LISTFILE = True
MAX_ALARMS = 21

list_of_alarms = []
alarms_sel = []
alarms_sel_sorted_2d = []
defaults_dict = {
    "PlayTime": "3",
    "AlarmSound": "generic_alarm.mp3",
    "Input": "Button",
    "Nap": "40",
}

alarm_sounds = os.listdir("./alarm_sounds")

#### THIS CODE WILL ADD 2 ALARMS ####
if ADD_2_ALARMS:
    d = datetime.now()
    min_1 = str(int(d.strftime("%M")) + 1)
    hours = d.strftime("%H")
    min_2 = str(int(d.strftime("%M")) + 2)
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
    sort_arr_time(list_of_alarms)
    alarms_sel_times = []
    for i in alarms_sel:
        alarms_sel_times.append(i.time)

    return render_template(
        "index.html",
        alarms_list=list_of_alarms,
        alarms_selcted=alarms_sel_times,
        alarm_sounds=alarm_sounds,
        defaults_dict=defaults_dict,
    )


#
# Function renders remove_alarm.html
#
@app.route("/removeablealarms", methods=["POST"])
def removeablealarms():
    return render_template("remove_alarm.html", alarms_list=list_of_alarms)


#
# Function renders settings.html
#
@app.route("/settings", methods=["POST"])
def settings():
    return render_template(
        "settings.html", alarm_sounds=alarm_sounds, defaults_dict=defaults_dict
    )


"""
FORM PROCESSES
"""
#
# Function will process nap button
#
@app.route("/timer_process", methods=["POST"])
def timer_process():
    time_change = timedelta(minutes=int(defaults_dict["Nap"]))
    new_time = (datetime.now() + time_change).strftime("%H:%M")

    for item in list_of_alarms:
        if new_time in item:
            flash("Alarm Already Exists!")
            return redirect(url_for("hello_world"))

    add_alarm = Alarm(
        new_time,
        playtime=defaults_dict["PlayTime"],
        alarm_sound=defaults_dict["AlarmSound"],
        input=defaults_dict["Input"],
    )

    list_of_alarms.append(add_alarm)
    # alarms_sel.append(add_alarm)

    return redirect(url_for("hello_world"))


#
# Function will update settings
#
@app.route("/update_settings", methods=['GET', 'POST'])
def update_settings():
    form_data = request.form
    
    defaults_dict["AlarmSound"] = form_data["alarm_sound_setting"]
    defaults_dict["Input"] = form_data["which_input_setting"]
    defaults_dict["PlayTime"] = form_data["playback_time_setting"]
    defaults_dict["Nap"] = form_data["nap_setting"]

    return redirect(url_for("hello_world"))

#
# Function will remove alarms from list
#
@app.route("/remove_alarms", methods=["POST"])
def remove_alarms():
    form_data = request.form
    form_checked = request.form.getlist("slider_box")

    remove_alarms_list(list_of_alarms, alarms_sel, form_checked)
    dump_data()

    return redirect(url_for("hello_world"))


#
# New function for getting new alarm form data
#
@app.route("/process_time", methods=["POST"])
def new_alarm():
    form_data = request.form
    new_time = form_data["time_prompt"]

    for item in list_of_alarms:
        if new_time in item:
            flash("Alarm Already Exists!")
            return redirect(url_for("hello_world"))

    add_alarm = Alarm(
        form_data["time_prompt"],
        playtime=form_data["playback_time"],
        alarm_sound=form_data["alarm_sound"],
        input=form_data["which_input"],
    )
    list_of_alarms.append(add_alarm)

    flash("Alarm " + new_time + " added!")
    return redirect(url_for("hello_world"))


"""
REQUEST HANDLERS
"""
#
# Function will handle request from checkbox.js
#
@app.route("/store_data", methods=["GET", "POST"])
def update_db():
    request_dict = request.get_json()
    checked = request_dict["checked"].copy()
    alarms_sel.clear()

    for checked in checked:
        for alarm in list_of_alarms:
            if checked in alarm:
                alarms_sel.append(alarm)

    dump_data()

    return request_dict

#
# Function will recieve request from ESP
#
@app.route("/detect", methods=['GET', 'POST'])
def detect():
    global data
    if request.method == 'POST':
        data = request.get_json()
        d = datetime.now()
        rn = d.strftime("%H:%M:%S")
        data["time"] = rn
        return 'Data received'
    elif request.method == 'GET':
        return data

#
# Function will recieve data from volume slider
#
@app.route("/volume_control", methods=["GET", "POST"])
def volume_control():
    global volume
    if request.method == "POST":
        volume = request.get_json()
        return "Data Received"
    elif request.method == "GET":
        return volume
        
"""
OTHER FUNCTIONS
"""
#
# Function will save alarms_sel into listfile.data using pickle
#
def dump_data():
    d = datetime.now()
    rn = d.strftime("%H:%M:%S")

    sort_arr_time(alarms_sel)
    with open("listfile.data", "wb") as alarms:
        pickle.dump([alarms_sel, rn], alarms)

#
# Function will remove alarms from list_of_alarms and selected_alarms
#
def remove_alarms_list(list_of_alarms, selected_alarms, form_checked):
    for time in form_checked:
        list_of_alarms[:] = [alarm for alarm in list_of_alarms if alarm.time != time]
        selected_alarms[:] = [alarm for alarm in list_of_alarms if alarm.time != time]

if __name__ == "__main__":
    if DEL_LISTFILE:
        if os.path.exists("listfile.data"):
            os.remove("listfile.data")
            print("removed listfile.data")
        else:
            print("listfile.data will be created")

        with open("listfile.data", "wb") as alarms:
            pickle.dump([[], 0], alarms)

    #p = Popen([sys.executable, '-u', './alarm.py'], stdout = PIPE, stderr=STDOUT, bufsize=1)
    app.run(host="0.0.0.0")

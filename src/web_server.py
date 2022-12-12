from flask import Flask, render_template, redirect, url_for, request, flash
from dotenv import load_dotenv, find_dotenv
import os

from datetime import datetime

from threading import Thread
import multiprocessing
import schedule
import time
from subprocess import Popen, PIPE, STDOUT
import sys
import pickle
from support_functions import sort_arr_time, sort_list

load_dotenv(find_dotenv())

app = Flask(__name__)
app.secret_key = os.getenv('app_secret')

list_of_alarms = ['18:45', '01:00', '10:15', '01:20', '00:01', '21:39']
alarms_selected = [] #['18:45', '01:00', '10:15', '01:20', '00:01', '22:40', '22:39']
diff_array = []

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
add_el = [1, now_1]
#diff_array.append(add_el)
add_el = [1, now_2]
#diff_array.append(add_el)

list_of_alarms.append(now_1)
list_of_alarms.append(now_2)
alarms_selected.append(now_1)
alarms_selected.append(now_2)

MINUTES_IN_DAY = 1440

"""
HTML PAGE RENDERING
"""
@app.route("/")
def hello_world():
    d = datetime.now()
    rn = d.strftime("%H:%M:%S")

    diff_array = sort_arr_time(alarms_selected)
    with open('listfile.data', 'wb') as alarms:
        pickle.dump([diff_array, rn], alarms)      

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

if __name__=="__main__":
    if os.path.exists("listfile.data"):
        os.remove("listfile.data")
        print("removed listfile.data")
    else:
        print("listfile.data will be created")

    p = Popen([sys.executable, '-u', './alarm.py'], stdout = PIPE, stderr=STDOUT, bufsize=1)
    app.run()

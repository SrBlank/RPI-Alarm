from flask import Flask, render_template, redirect, url_for, request, flash
from dotenv import load_dotenv, find_dotenv
import os
load_dotenv(find_dotenv())

app = Flask(__name__)
app.secret_key = os.getenv('app_secret')

list_of_alarms = ['18:45', '01:00', '10:15', '01:20']
alarms_selected = ['18:45', '01:00']

@app.route("/")
def hello_world():
    return render_template(
        "index.html",
        alarms_list = list_of_alarms,
        alarms_selcted = alarms_selected
        )

@app.route("/removeablealarms", methods=['POST'])
def removeablealarms():
    return render_template(
        "remove_alarm.html",
        alarms_list = list_of_alarms
        )

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
    sort_list()
    
    return redirect(url_for("hello_world"))

#
# Function will sort the array from the earliest to latest time 
#
def sort_list():
    for i in range(1,len(list_of_alarms)):
        for j in range(0, len(list_of_alarms)-1):
            hours_current = list_of_alarms[j][0] + list_of_alarms[j][1]
            minutes_current = list_of_alarms[j][3] + list_of_alarms[j][4]
            hours_next = list_of_alarms[j+1][0] + list_of_alarms[j+1][1]
            minutes_next = list_of_alarms[j][3] + list_of_alarms[j][4]

            if int(hours_current) >= int(hours_next) :
                if int(minutes_current) <= int(minutes_next):
                    temp = hours_current + ':' + minutes_current
                    list_of_alarms[j] = list_of_alarms[j+1]
                    list_of_alarms[j+1] = temp
    
if __name__=="__main__":
    app.run()

 
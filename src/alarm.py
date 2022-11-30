import time
from threading import Thread
from datetime import datetime 
#from web_server import alarms_selected


def checkTime():
    for i in range(10):
        time.sleep(1)
        print(i)

class Alarm:
    def __init__(self, alarm):
        self.alarm = alarm
        self.thread.start()

    def __del__(self):
        del self.alarm
        #self.thread.join()
        del self.thread


    def getAlarmTime(self):
        return self.alarm

    #self.alarm
    thread = Thread(target = checkTime, daemon=False)

t = Alarm("hello")
print(t.getAlarmTime())
del t
print("hello")



#t = Alarm("hello")
#print(t.getAlarmTime())

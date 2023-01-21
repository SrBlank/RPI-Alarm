
class Alarm():
    def __init__(self):
        self.time = "--:--"
        self.playtime = 3
        self.button = True
        self.alarm_sound = "./alarm_sounds/generic_alarm.mp3" 


d = Alarm()
print(d.time)
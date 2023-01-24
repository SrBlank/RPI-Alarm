
class Alarm(object):
    def __init__(self, time, playtime=3):
        self.time = time
        self.playtime = playtime
        self.button = True
        self.alarm_sound = "./alarm_sounds/generic_alarm.mp3" 
    
    def __repr__(self):
        return self.time  + " " + str(self.playtime) 
    def __contains__(self, item):
        return item in self.time
""" 
employees = [
    Alarm('11:11', 4),
    Alarm('12:20', 3),
    Alarm('1:20', 21)
]
print(employees)

# sort list by `name` in the natural order
employees.sort(key=lambda x: x.time)

# output: [{Joe, Finance, 25}, {John, IT, 28}, {Sam, Banking, 20}]
print(employees)
"""
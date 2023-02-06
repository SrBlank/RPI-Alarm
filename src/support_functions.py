from datetime import datetime, timedelta

def sort_arr_time(list_of_alarms):
    current_datetime = datetime.now()
    current_time = current_datetime.time()
    
    def diff(alarm):
        alarm_datetime = current_datetime.replace(hour=int(alarm.time[:2]), minute=int(alarm.time[3:]))
        if alarm_datetime < current_datetime:
            alarm_datetime += timedelta(days=1)
        return (alarm_datetime - current_datetime).seconds
    
    list_of_alarms.sort(key=diff)


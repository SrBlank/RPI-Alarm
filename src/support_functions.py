from datetime import datetime

from alarm_class import Alarm

MINUTES_IN_DAY = 1440

#
# sort_arr_time
# Takes a 1d array of time as input Ex: ["01:15", "23:45", "00:00"]
# Returns a sortted 2d array of [time difference, "time"] with respect to the current time
#
def sort_arr_time(D1_array_to_sort):
    sorted_array = []
    if len(D1_array_to_sort) != 0:
        temp_array = []
        for i in range(0, len(D1_array_to_sort)):
            temp_array.append(D1_array_to_sort[i])

        d = datetime.now()
        formatted_d = d.strftime("%H:%M")
        hoursC = d.strftime("%H")
        minutesC = d.strftime("%M")
        conver_min = int(hoursC)*60 + int(minutesC)

        #for i in range(0, len(temp_array)):
        for i in temp_array:
            hours_current = i.time[0] + i.time[1] #temp_array[i][0] + temp_array[i][1]
            minutes_current = i.time[3] + i.time[4] #temp_array[i][3] + temp_array[i][4]
            conver_current = int(hours_current)*60 + int(minutes_current)

            difference = conver_current - conver_min
            if (difference > 0):
                i.time_diff = difference
                #index_b_time = [difference, i]#hours_current + ":" + minutes_current]
                sorted_array.append(i)
            elif (difference <= 0):
                i.time_diff = MINUTES_IN_DAY-(difference*-1)
                #index_b_time = [MINUTES_IN_DAY-(difference*-1), i]#hours_current + ":" + minutes_current]
                sorted_array.append(i)
        sorted_array.sort(key=lambda x: x.time_diff)
        return sorted_array 
    else:
        pass


from datetime import datetime

from alarm_class import Alarm

MINUTES_IN_DAY = 1440

# sort_arr_time
# Takes a 1d array of time as input Ex: ["01:15", "23:45", "00:00"]
# Returns a sortted 2d array of [time difference, "time"] with respect to the current time

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


"""
DEPRECATED
"""
# sort_list
# takes in a 1d array of times ["01:15", "23:45", "00:00"]
# Returns sorted 1d array of times from 00:00 to 23:59 ["00:00", "01:15", "23:45"]
"""
def sort_list(sort_array):
    #print(sort_array)
    return sort_array.sort(key=lambda x: x.time)
    #print(sort_array)

    #return sort_array.sort(key=lambda x: x.time)
    #return sorted(sort_array)
"""


"""
DEPRECATED
"""
# sort_arr_time_2d
# takes a 2d array of [time difference, "time"] as input
# converts the 2d array into a 1d array of times then calls sort_arr_time
# Returns a sortted 2d array of [time difference, "time"] with respect to the current time
"""
def sort_arr_time_2d(D2_array_to_sort=[]):
    if len(D2_array_to_sort) != 0:
        temp_array = []
        for i in range(0, len(D2_array_to_sort)):
            temp_array.append(D2_array_to_sort[i][1])

        sorted_array = sort_arr_time(temp_array)

        return sorted_array 
    else:
        pass
"""


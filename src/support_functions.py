from datetime import datetime

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

        for i in range(0, len(temp_array)):
            hours_current = temp_array[i][0] + temp_array[i][1]
            minutes_current = temp_array[i][3] + temp_array[i][4]
            conver_current = int(hours_current)*60 + int(minutes_current)

            difference = conver_current - conver_min
            if (difference > 0):
                index_b_time = [difference, hours_current + ":" + minutes_current]
                sorted_array.append(index_b_time)
            elif (difference <= 0):
                index_b_time = [MINUTES_IN_DAY-(difference*-1), hours_current + ":" + minutes_current]
                sorted_array.append(index_b_time)
        sorted_array.sort(key=lambda x: x[0])
        return sorted_array 
    else:
        pass

# sort_arr_time_2d
# takes a 2d array of [time difference, "time"] as input
# converts the 2d array into a 1d array of times then calls sort_arr_time
# Returns a sortted 2d array of [time difference, "time"] with respect to the current time
def sort_arr_time_2d(D2_array_to_sort=[]):
    if len(D2_array_to_sort) != 0:
        temp_array = []
        for i in range(0, len(D2_array_to_sort)):
            temp_array.append(D2_array_to_sort[i][1])

        sorted_array = sort_arr_time(temp_array)

        return sorted_array 
    else:
        pass

# sort_list
# takes in a 1d array of times ["01:15", "23:45", "00:00"]
# Returns sorted 1d array of times from 00:00 to 23:59 ["00:00", "01:15", "23:45"]
def sort_list(sort_array):
    for i in range(1,len(sort_array)):
        for j in range(0, len(sort_array)-1):
            hours_current = sort_array[j][0] + sort_array[j][1]
            minutes_current = sort_array[j][3] + sort_array[j][4]
            hours_next = sort_array[j+1][0] + sort_array[j+1][1]
            minutes_next = sort_array[j][3] + sort_array[j][4]

            if int(hours_current) >= int(hours_next) :
                if int(minutes_current) <= int(minutes_next):
                    temp = hours_current + ':' + minutes_current
                    sort_array[j] = sort_array[j+1]
                    sort_array[j+1] = temp
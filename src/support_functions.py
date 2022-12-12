from datetime import datetime

MINUTES_IN_DAY = 1440

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

def sort_arr_time_2d(D2_array_to_sort=[]):
    if len(D2_array_to_sort) != 0:
        temp_array = []
        for i in range(0, len(D2_array_to_sort)):
            temp_array.append(D2_array_to_sort[i][1])

        sorted_array = sort_arr_time(temp_array)

        return sorted_array 
    else:
        pass
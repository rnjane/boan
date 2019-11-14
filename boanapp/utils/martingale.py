ls = [0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0]
time_ls = [(-1, datetime.datetime(2019, 7, 26, 1, 20, tzinfo= < UTC >)),
           (-1, datetime.datetime(2019, 7, 26, 1, 21, tzinfo= < UTC > )),
           (-1, datetime.datetime(2019, 7, 26, 1, 22, tzinfo= < UTC >)),
           (0, datetime.datetime(2019, 7, 26, 1, 23, tzinfo= < UTC > )),
           (-1, datetime.datetime(2019, 7, 26, 1, 24, tzinfo= < UTC >)),
           (-1, datetime.datetime(2019, 7, 26, 1, 25, tzinfo= < UTC > )),
           (-1, datetime.datetime(2019, 7, 26, 1, 26, tzinfo= < UTC >)),
           (-1, datetime.datetime(2019, 7, 26, 1, 27, tzinfo= < UTC > )),
           (-1, datetime.datetime(2019, 7, 26, 1, 28, tzinfo= < UTC >)),
           (-1, datetime.datetime(2019, 7, 26, 1, 29, tzinfo= < UTC > ))]


def new_array(old_array):
    new_list = []
    for element in old_array:
        if element == 0:
            pass
        elif element == 1:
            new_list.append(element)
        elif element == -1:
            new_list.append(0)
    return new_list


def new_array_with_time(old_array):
    new_list = []
    for element in old_array:
        if element[0] == 0:
            pass
        elif element[0] == 1:
            new_list.append(element)
        elif element[0] == -1:
            new_list.append((0, element[1]))
    return new_list


def return_martin(input_array):
    input_array = new_array(input_array)
    returned_list = []
    previous = 0
    zero_count = 0
    for i in input_array:
        if i == 0 and previous == 1:
            zero_count = 1
            previous = 0
        elif i == 0 and previous == 0:
            zero_count += 1
            previous = 0
        elif i == 1 and zero_count > 0:
            returned_list.append(zero_count)
            zero_count = 0
            previous = 1
    if zero_count > 0:
        returned_list.append(zero_count)
    return sorted(returned_list, reverse=True)


def return_martin_with_time(input_array):
    input_array = new_array_with_time(input_array)
    returned_list = []
    previous = 0
    zero_count = 0
    start_time = None
    for i in input_array:
        if i[0] == 0 and previous == 1:
            start_time = i[1]
            zero_count = 1
            previous = 0
        elif i[0] == 0 and previous == 0:
            zero_count += 1
            previous = 0
        elif i[0] == 1 and zero_count > 0:
            returned_list.append((zero_count, (start_time, i[1])))
            start_time = None
            zero_count = 0
            previous = 1
    if zero_count > 0:
        returned_list.append(zero_count)
    return returned_list


print(return_martin(ls))

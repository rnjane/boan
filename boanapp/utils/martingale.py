ls = [0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0]


def return_martin(input_array):
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
        elif i == and zero_count > 0:
            returned_list.append(zero_count)
            zero_count = 0
            previous = 1
    return returned_list


print(return_martin(ls))

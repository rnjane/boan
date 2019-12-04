ls = [0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1]


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


def mgalr_calculator(input_array):
    profit = 0
    current_value = 1
    zero_count = 0
    cv_list = [1.0, 2.25, 5.06, 11.39, 25.63, 57.67, 129.75]
    x = new_array(input_array[:25])
    for i in x:
        if i == 1:
            profit += current_value * 0.8
            zero_count = 0
            current_value = 1
        elif i == 0:
            profit -= current_value
            if zero_count == 4:
                current_value = 1
                zero_count = 0
            zero_count += 1
            current_value = cv_list[zero_count]
        # print("Current profit is {}".format(round(profit, 2)))
    return profit


print(mgalr_calculator(ls))

'''
starting_array = [1,2]
current_number = method
If 1, and hole is zero, just increment the profit.
If 0, and hole is zero:
1. add arr[0] and arr[n] to the end of the array
2. Get the corresponding increase in hole, and do new assignment.
3. Increment the loss by arr[0] + arr[n]
If 1, and hole > 0:
1. use current number
1. reduce hole by 1.
2. try to reduce size by 2, if fails at 1, reduce by 1.
'''
import math

current_array = [1, 2]
profit = 0
loss = 0
hole = 0


def calculate_current_value():
    global current_array
    if current_array == []:
        current_array = [1, 2]
    size = len(current_array)
    if size == 1:
        return current_array[0]
    return current_array[0] + current_array[size - 1]


def increase_array():
    global current_array
    size = len(current_array)
    if size == 1:
        new_element = current_array[0]
    else:
        new_element = current_array[0] + current_array[size - 1]
    current_array.append(new_element)
    return current_array


def reduce_array():
    global current_array
    if len(current_array) == 0:
        current_array = [1, 2]
    elif len(current_array) == 1:
        del current_array[0]
    else:
        del current_array[-1]
        del current_array[0]
    return current_array


def calculate_hole():
    global current_array
    global hole
    size = len(current_array)
    if size == 0:
        hole = 0
    else:
        hole = int(math.ceil(size/2))
    return hole


def prophet(oneorzero):
    global profit
    global loss
    if oneorzero == 1 and hole == 0:
        profit += 3
        calculate_hole()
    elif oneorzero == 0 and hole == 0:
        profit -= calculate_current_value()
        increase_array()
        calculate_hole()
    elif oneorzero == 0 and hole > 0:
        profit -= calculate_current_value()
        increase_array()
        calculate_hole()
    elif oneorzero == 1 and hole > 0:
        profit += calculate_current_value()
        reduce_array()
        calculate_hole()
    return profit


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


def get_profit(arr):
    for i in new_array(arr):
        prophet(i)
        # print("Hole is {0} and profit is {1} and current array is {2}".format(
        #     hole, profit, current_array))
    return profit


print(get_profit([0, 0, -1, -1, 1, -1, 1, -1, 1, -1, -1, 1, -1, 1, 1, -1, 0, 1, 1, 1, 1, -1, 1, 1, -1, 1, -1, -1, -1,
                  1, -1, 1, 1, 1, -1, -1, 1, 1, 0, -1, -1, -1, -1, 1, 1, 1, -1, 1, 1, 1, 1, 1, -1, -1, -1, -1, 1, -1, -1, -1]))

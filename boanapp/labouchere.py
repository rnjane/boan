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

# current_array = [1, 2]
# profit = 0
# loss = 0
# hole = 0


class ProphetC():
    def __init__(self, current_array=[1, 2], profit=0, hole=0):
        self._current_array = current_array
        self._profit = profit
        self._hole = hole

    def set_current_array(self, lst):
        self._current_array = lst

    def set_profit(self, p):
        self._profit = p

    def set_hole(self, h):
        self._hole = h

    def calculate_current_value(self):
        if self._current_array == []:
            self.set_current_array([1, 2])
        size = len(self._current_array)
        if size == 1:
            return self._current_array[0]
        return self._current_array[0] + self._current_array[size - 1]

    def increase_array(self):
        size = len(self._current_array)
        if size == 1:
            new_element = self._current_array[0]
        else:
            new_element = self._current_array[0] + \
                self._current_array[size - 1]
        self._current_array.append(new_element)
        return self._current_array

    def reduce_array(self):
        if len(self._current_array) == 0:
            self.set_current_array([1, 2])
        elif len(self._current_array) == 1:
            del self._current_array[0]
        else:
            del self._current_array[-1]
            del self._current_array[0]
        return self._current_array

    def calculate_hole(self):
        size = len(self._current_array)
        if size == 0:
            self._hole = 0
        else:
            self._hole = int(math.ceil(size/2))
        return self._hole

    def prophet(self, oneorzero):
        if oneorzero == 1 and self._hole == 0:
            self._profit += 3
            self.calculate_hole()
        elif oneorzero == 0 and self._hole == 0:
            self._profit -= self.calculate_current_value()
            self.increase_array()
            self.calculate_hole()
        elif oneorzero == 0 and self._hole > 0:
            self._profit -= self.calculate_current_value()
            self.increase_array()
            self.calculate_hole()
        elif oneorzero == 1 and self._hole > 0:
            self._profit += self.calculate_current_value()
            self.reduce_array()
            self.calculate_hole()
        return self._profit

    def new_array(self, old_array):
        new_list = []
        for element in old_array:
            if element == 0:
                pass
            elif element == 1:
                new_list.append(element)
            elif element == -1:
                new_list.append(0)
        return new_list

    def get_profit(self, arr):
        for i in self.new_array(arr):
            self.prophet(i)
            # print("Hole is {0} and profit is {1} and current array is {2}".format(
            #     self._hole, self._profit, self._current_array))
        return self._profit


# cl = ProphetC()
# print(cl.get_profit([0, 0, -1, -1, 1, -1, 1, -1, 1, -1, -1, 1, -1, 1, 1, -1, 0, 1, 1, 1, 1, -1, 1, 1, -1, 1, -1, -1, -1,
#                      1, -1, 1, 1, 1, -1, -1, 1, 1, 0, -1, -1, -1, -1, 1, 1, 1, -1, 1, 1, 1, 1, 1, -1, -1, -1, -1, 1, -1, -1, -1]))

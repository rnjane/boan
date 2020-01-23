array = [1,2]
k = 0.7

while True:
    success = input('Success?')
    if success == 'y':
        if len(array) > 2:
            del array[0]
            del array[-1]
            val = sum([array[0], array[-1]])
        elif len(array) == 1:
            val = array[0]
            array = [1,2]
        else:
            val = sum([array[0], array[-1]])
            array = [1,2]
        print('Current array is {}'.format(array))
        print('next is {}'.format(val))
    else:
        val = sum([array[0], array[-1]]) / k
        val = round(val, 1)
        array.append(val)
        print('Current array is {}'.format(array))
        print('next is {}'.format(val))

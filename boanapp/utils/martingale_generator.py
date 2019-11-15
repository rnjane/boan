def martingale():
    returned_list = []
    all_losses = 0
    for i in range(1, 10):
        y = all_losses / 0.8
        returned_list.append(round(y + 1, 2))
        all_losses += (y + 1)
    return returned_list


a = martingale()
print(a)
print([round(sum(a[:x+1]), 2) for x in range(0, len(a))])

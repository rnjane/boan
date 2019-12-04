from boanapp import models


def get_moneies_list(asset, year, month, date):
    """
    return a list of ones and zero to be fed to the labouchere algorithm
    """
    # money_dict = {}
    # for i in range(24):
    #     queryset = models.ValuesMA.objects.filter(
    #         pair=asset, timer__year=year, timer__month=month, timer__day=date, timer__hour=i).values("money").order_by('timer')
    #     money_list = [record['money'] for record in queryset]
    #     money_dict[i] = money_list
    # return money_dict

    money_dict = {}
    for i in range(24):
        queryset = models.ValuesLen.objects.filter(
            pair=asset, timer__year=year, timer__month=month, timer__day=date, timer__hour=i, ignore=False).values("money").order_by('timer')
        money_list = [record['money'] for record in queryset]
        money_dict[i] = money_list
    return money_dict


def get_start_date():
    start_date = models.ValuesMA.objects.filter(
        pair="AUDUSD").values("timer").order_by('id')[0]
    return start_date['timer'].strftime("%m/%d/%Y")


def get_last_date():
    return "04/18/2018"

    # last_date = models.ValuesMAComplete.objects.filter(
    #     pair="AUDUSD").values("timer").last()
    # # last_date = models.ValuesMAComplete.objects.filter(
    # #     pair="AUDUSD").values("timer").order_by('-id')[0]
    # return last_date['timer'].strftime("%m/%d/%Y")


def get_percents():
    percents_dict = {}
    for asset in ["GBPJPY"]:
        print('working on {}'.format(asset))
        a = ValuesMA7.objects.filter(
            pair=asset).values("money", "timer")
        c = [(record['money'], record['timer'])
             for record in a]
        e = return_martin_with_time(c)
        percent = (len(e) / len(c)) * 100
        percents_dict[asset] = percent
    return percents_dict


# a = ValuesMA7.objects.filter(
#     pair="GBPJPY").values("money", "timer")
# c = [(record['money'], record['timer'])
#      for record in a]
# e = return_martin_with_time(c)

# a = ValuesMA7.objects.filter(
#     pair="GBPJPY").values("money", "timer")
# c = [record['money'] for record in a]
# e = mgalr_calculator(c)

# queryset = ValuesMA.objects.filter(
#     pair="AUDCAD", timer__year=2019, timer__month=7, timer__day=25, timer__hour=17).values("money", "timer").order_by('id')
# money_list = [(record['money'], record['timer']) for record in queryset]

# e = return_martin_with_time(money_list)

from boanapp import models


def get_moneies_list(asset, year, month, date):
    """
    return a list of ones and zero to be fed to the labouchere algorithm
    """
    money_dict = {}
    for i in range(23):
        queryset = models.ValuesMA.objects.filter(
            pair=asset, timer__year=year, timer__month=month, timer__day=date, timer__hour=i).values("money").order_by('timer')
        money_list = [record['money'] for record in queryset]
        money_dict[i] = money_list
    return money_dict


def get_start_date():
    start_date = models.ValuesMA.objects.filter(
        pair="AUDUSD").values("timer").order_by('id')[0]
    return start_date['timer'].strftime("%m/%d/%Y")


def get_last_date():
    last_date = models.ValuesMA.objects.filter(
        pair="AUDUSD").values("timer").order_by('-id')[0]
    return last_date['timer'].strftime("%m/%d/%Y")

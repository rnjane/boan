from boanapp import models


def get_moneies_list(asset):
    """
    return a list of ones and zero to be fed to the labouchere algorithm
    """
    money_dict = {}
    for i in range(23):
        queryset = models.ValuesMA.objects.filter(
            pair=asset, timer__year=2019, timer__month=7, timer__day=26, timer__hour=i).values("money").order_by('timer')
        money_list = [record['money'] for record in queryset]
        money_dict[i] = money_list
    return money_dict

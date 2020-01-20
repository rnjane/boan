from boanapp import models
from django.apps import apps

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


def get_percents(table, ma):
    percents_dict = {}
    for asset in ["GBPJPY"]:
        print('working on {0} for table {1}'.format(asset, table))
        a =  apps.get_model('boanapp', table).objects.filter(candle__pair=asset).values(ma + "money", "candle__candle_time")
        c = [(record[ma + "money"], record['candle__candle_time'])
             for record in a]
        e = return_martin_with_time(c)
        percent = (len(e) / len(c)) * 100
        percents_dict[asset] = percent
    return percents_dict

def return_percents():
    tables = ["OneMinuteMovingAverage", "TwoMinuteMovingAverage", "FiveMinuteMovingAverage", "TenMinuteMovingAverage", "FifteenMinuteMovingAverage"]
    mas = ["sma5", "sma10", "sma15", "sma20", "sma25", "sma30", "sma60", "ema5", "ema10", "ema15", "ema20", "ema25", "ema30", "ema60","wma5", "wma10", "wma15", "wma20", "wma25", "wma30", "wma60"]
    res = {}
    for table in tables:
        for ma in mas:
            res[table + ma] = get_percents(table, ma)['GBPJPY']
    return res

# a = OneMinuteMovingAverage.objects.filter(
#     candle__pair=asset).values("sma20money", "candle__candle_time")
# c = [(record['sma20money'], record['candle__candle_time'])
#      for record in a]
# e = return_martin_with_time(c)

# # a = ValuesMA7.objects.filter(
# #     pair="GBPJPY").values("money", "timer")
# # c = [record['money'] for record in a]
# # e = mgalr_calculator(c)

# queryset = OneMinuteMovingAverage.objects.filter(
#     candle__pair=asset, candle__candle_time__year=2019, candle__candle_time__month=11, candle__candle_time__day=20).values("sma20money", "candle__candle_time").order_by('id')
# money_list = [(record['sma20money'], record['candle__candle_time']) for record in queryset]
# e = return_martin_with_time(money_list)

def get_value_by_date():
    vals = OneMinuteCandle.objects.filter(
            pair="AUDCAD", candle_time__year=2019, candle_time__month=11, candle_time__day=29, candle_time__hour=13)
    money_list = [(record.candle_time.strftime("%m/%d/%Y, %H:%M:%S"), record.candle_max, record.candle_close) for record in vals]
    return money_list

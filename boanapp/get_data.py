import time
import datetime
import os
import json
import ast
import csv
import pytz
from iqoptionapi.stable_api import IQ_Option as api
import pandas as pd
from sqlalchemy import *
assets = [
    "AUDUSD", "AUDCAD", "USDCHF", "EURNOK", "AUDNZD", "GBPJPY", "EURAUD", "AUDCHF", "GBPCHF",
    "GBPNZD", "EURGBP", "EURCAD", "EURNZD", "NZDCAD", "GBPCAD", "USDJPY", "NZDCHF", "USDNOK",
    "EURUSD", "NZDJPY", "CADJPY", "GBPUSD", "AUDJPY", "USDCAD", "EURJPY", "CADCHF", "USDJPY-OTC",
    "EURUSD-OTC", "EURGBP-OTC", "USDCHF-OTC", "EURJPY-OTC", "NZDUSD-OTC", "AUDCAD-OTC",
    "GBPUSD-OTC", "EURRUB-OTC", "USDRUB-OTC", "GBPJPY-OTC"
]


def convert_date_time_to_epoch(inputdate):
    timestamp = time.mktime(time.strptime(inputdate, '%Y-%m-%d %H:%M'))
    return timestamp


def generate_times():
    finish_time = 1564174799
    times_list = []
    for i in range(10):
        converted_time = datetime.datetime.fromtimestamp(
            finish_time, pytz.timezone("Africa/Nairobi")
        ).strftime("%Y-%m-%d %H:%M:%S")
        df = pd.Timestamp(converted_time)
        if df.dayofweek in range(0, 5):
            times_list.append(finish_time)
        finish_time -= 43200
    return times_list


def get_values():
    iqemail = os.environ.get('iqemail')
    iqpasswd = os.environ.get('iqpassword')
    try:
        vals = api(iqemail, iqpasswd)
        print('successfully logged in')
    except Exception as e:
        print('Could not log in because of {0}'.format(e))

    engine = create_engine(os.environ.get('sqlalchemy_uri'))
    connection = engine.connect()
    metadata = MetaData()
    my_table = Table("boanapp_values", metadata, autoload_with=engine)
    for instrument in assets:
        print("getting values for {}".format(instrument))
        times = generate_times()
        for time in times:
            cdle_list = []
            my_candles = vals.get_candles(instrument, 60, 500, time)
            for candle in my_candles:
                cdle = ast.literal_eval(json.dumps(candle))
                del cdle["at"]
                del cdle["to"]
                del cdle["id"]
                del cdle["volume"]
                from_time = cdle["from"]
                from_time_converted = datetime.datetime.fromtimestamp(
                    from_time, pytz.timezone("Africa/Nairobi")
                ).strftime("%Y-%m-%d %H:%M:%S")
                del cdle["from"]
                cdle["timer"] = from_time_converted
                cdle["pair"] = instrument
                greenred = cdle["close"] - cdle["open"]
                if greenred < 0:
                    cdle["greenred"] = -1
                elif greenred == 0:
                    cdle["greenred"] = 0
                else:
                    cdle["greenred"] = 1

                wkday = pd.Timestamp(from_time_converted)
                if wkday.weekday() in range(0, 5):
                    cdle_list.append(cdle)
                else:
                    pass
            # print("Saving values for {}".format(instrument))
            connection.execute(my_table.insert(), cdle_list)


get_values()

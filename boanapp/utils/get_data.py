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


# assets = [
#     "AUDUSD", "AUDCAD", "USDCHF", "EURNOK", "AUDNZD", "GBPJPY", "EURAUD", "AUDCHF", "GBPCHF",
#     "GBPNZD", "EURGBP", "EURCAD", "EURNZD", "NZDCAD", "GBPCAD", "USDJPY", "NZDCHF", "USDNOK",
#     "EURUSD", "NZDJPY", "CADJPY", "GBPUSD", "AUDJPY", "USDCAD", "EURJPY", "CADCHF"
# ]

assets = [
    "EURUSD", "NZDJPY", "CADJPY", "GBPUSD", "AUDJPY", "USDCAD", "EURJPY", "CADCHF"
]

assets_otc = [
    "EURUSD-OTC", "EURGBP-OTC", "USDCHF-OTC", "EURJPY-OTC", "NZDUSD-OTC", "AUDCAD-OTC",
    "GBPUSD-OTC", "USDJPY-OTC"
]

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
my_table = Table("boanapp_valuescomplete", metadata, autoload_with=engine)
days = 360
end_date = 1575071999

def convert_date_time_to_epoch(inputdate):
    timestamp = time.mktime(time.strptime(inputdate, '%Y-%m-%d %H:%M'))
    return timestamp

def generate_time_intervals(time_interval, number_of_days):
    y = (60 * 24) / time_interval
    if y > 1000:
        z = y / 2
        return int(z * 60), int(number_of_days * 2)
    else:
        a = 1000 // y
        return int(y * 60 * a * time_interval), int(number_of_days / a)

def generate_times_f(time_interval):
    returned_times = {"Live": [], "OTC": []}
    end_date = 1575071999
    time_values = generate_time_intervals(time_interval, days)
    for i in range(time_values[1]):
        converted_time = datetime.datetime.fromtimestamp(
            end_date, pytz.timezone("GMT")
        ).strftime("%Y-%m-%d %H:%M:%S")
        df = pd.Timestamp(converted_time)
        if df.dayofweek in range(0, 5):
            returned_times['Live'].append(end_date)
        elif df.dayofweek in range(5, 7):
            returned_times['OTC'].append(end_date)
        end_date -= time_values[0]
    return returned_times

def get_candles(time, )

def return_vals(asset, passed_time):
    cdle_list = []
    my_candles = vals.get_candles(asset, 60, 1000, passed_time)
    for candle in my_candles:
        cdle = ast.literal_eval(json.dumps(candle))
        del cdle["at"]
        del cdle["to"]
        del cdle["id"]
        del cdle["volume"]
        from_time = cdle["from"]
        from_time_converted = datetime.datetime.fromtimestamp(
            from_time, pytz.timezone("GMT")
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
    return cdle_list

def get_values():
    for instrument in assets:
        print("getting values for {}".format(instrument))
        for time in generate_times():
            values = return_vals(instrument, time)
            connection.execute(my_table.insert(), cdle_list)

get_values()
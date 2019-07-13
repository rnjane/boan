import time
import datetime
import os
from iqoptionapi.stable_api import IQ_Option as api
import json
import ast
import csv
import pytz
import pandas as pd

from sqlalchemy import *

from . import models


def convert_date_time_to_epoch(inputdate):
    timestamp = time.mktime(time.strptime(inputdate, '%Y-%m-%d %H:%M'))
    return timestamp


def generate_times(finishtime, number_of_semi_days):
    finish_time = convert_date_time_to_epoch(finishtime)
    times_list = []
    for i in range(number_of_semi_days):
        converted_time = datetime.datetime.fromtimestamp(
            finish_time, pytz.timezone("Africa/Nairobi")
        ).strftime("%Y-%m-%d %H:%M:%S")
        df = pd.Timestamp(converted_time)
        if df.dayofweek in range(0, 5):
            times_list.append(finish_time)
        finish_time -= 43200
    return times_list


def get_values(asset, finish_time, number_of_semi_days, candle_time):
    iqemail = os.environ.get('iqemail')
    iqpasswd = os.environ.get('iqpasswd')
    try:
        vals = api(iqemail, iqpasswd)
        print('successfully logged in')
    except Exception as e:
        print('Could not log in because of {0}'.format(e))

    epoch_times = generate_times(finish_time, number_of_semi_days)
    for epoch_time in epoch_times:
        cdle_list = []
        my_candles = vals.get_candles(asset, candle_time, 500, epoch_time)
        for candle in my_candles:
            cdle = ast.literal_eval(json.dumps(candle))
            del cdle['at']
            del cdle['to']
            del cdle['id']
            del cdle['volume']
            from_time = cdle['from']
            from_time_converted = datetime.datetime.fromtimestamp(
                from_time, pytz.timezone('Africa/Nairobi')).strftime('%Y-%m-%d %H:%M:%S')
            del cdle['from']
            cdle['timer'] = from_time_converted
            cdle['pair'] = asset
            x = cdle['close'] - cdle['open']
            if x < 0:
                cdle['greenred'] = -1
            elif x == 0:
                cdle['greenred'] = 0
            else:
                cdle['greenred'] = 1
            cdle_list.append(cdle)
        connection.execute(my_table.insert(), cdle_list)

    # keys = cdle_list[0].keys()
    # with open('nzdusd.csv', 'wb') as output_file:
    #     dict_writer = csv.DictWriter(output_file, keys)
    #     dict_writer.writeheader()
    #     dict_writer.writerows(cdle_list)

    engine = create_engine(
        'postgresql+psycopg2://robertnjane:roba1234@localhost/dataf')
    connection = engine.connect()

    metadata = MetaData()

    my_table = Table('dataapp_values', metadata, autoload_with=engine)

    connection.execute(my_table.insert(), cdle_list)
    keys = cdle_list[0].keys()
    with open('data.csv', 'wb') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(cdle_list)
        import pdb
        pdb.set_trace()


get_values()

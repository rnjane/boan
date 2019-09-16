import psycopg2
from sqlalchemy import extract, Table, create_engine, MetaData, desc, asc
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
import pandas as pd
import os
import labouchere
from datetime import datetime

engine = create_engine(os.environ.get('sqlalchemy_uri'))
connection = engine.connect()
metadata = MetaData()

Session = sessionmaker(bind=engine)
session = Session()

length_table = Table("boanapp_valueslen", metadata, autoload_with=engine)


def new_array(old_array):
    new_list = []
    for element in old_array:
        if element == 0:
            pass
        elif element == 1:
            new_list.append(element)
        elif element == -1:
            new_list.append(0)
    return new_list


def get_last_date(table):
    return session.query(table).filter_by(pair='AUDUSD').order_by(desc('timer')).first().timer.strftime("%m/%d/%Y")


def get_start_date(table):
    return session.query(table).filter_by(pair='AUDUSD').order_by(asc('timer')).first().timer.strftime("%m/%d/%Y")


def get_all_dates(table):
    all_dates = pd.date_range(start=get_start_date(table),
                              end=get_last_date(table)).strftime("%m/%d/%Y").to_list()
    return all_dates


def get_moneies_list(table, asset, year, month, date):
    money_dict = {}
    for i in range(24):
        queryset = session.query(length_table).filter_by(pair=asset, ignore=False).filter(
            extract('year', length_table.c.timer) == year, extract(
                'month', length_table.c.timer) == month, extract('day', length_table.c.timer) == date, extract('hour', length_table.c.timer) == i).all()
        money_dict[i] = new_array([record.money for record in queryset])
    return money_dict


def get_hourly_profit(asset):
    for date in get_all_dates(length_table):
        split_date = date.split('/')
        try:
            lst = get_moneies_list(
                length_table, asset, split_date[2], split_date[0], split_date[1])
            mlist = []
            for key, value in lst.items():
                ddict = {}
                profit = labouchere.ProphetC().get_profit(value)
                dtime = datetime.strptime(date + " " + str(key), '%m/%d/%Y %H')
                ddict['asset'] = asset
                ddict['dtime'] = dtime
                ddict['profits'] = profit
                mlist.append(ddict)
            table2 = Table("boanapp_hourlyprofit",
                           metadata, autoload_with=engine)
            connection.execute(table2.insert(), mlist)
        except Exception as e:
            raise e
    return f"done with {asset}"


assets = [
    "AUDUSD", "AUDCAD", "USDCHF", "EURNOK", "AUDNZD", "GBPJPY", "EURAUD", "AUDCHF", "GBPCHF",
    "GBPNZD", "EURGBP", "EURCAD", "EURNZD", "NZDCAD", "GBPCAD", "USDJPY", "NZDCHF", "USDNOK",
    "EURUSD", "NZDJPY", "CADJPY", "GBPUSD", "AUDJPY", "USDCAD", "EURJPY", "CADCHF", "USDJPY-OTC",
    "EURUSD-OTC", "EURGBP-OTC", "USDCHF-OTC", "EURJPY-OTC", "NZDUSD-OTC", "AUDCAD-OTC",
    "GBPUSD-OTC", "EURRUB-OTC", "USDRUB-OTC", "GBPJPY-OTC"
]

for asset in assets:
    print("Working on {}".format(asset))
    profits = get_hourly_profit(asset)
    print(profits)

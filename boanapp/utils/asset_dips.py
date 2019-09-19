import psycopg2
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
import pandas as pd
from talib import abstract
import os


queryset = session.query(length_table).filter_by(pair=asset).all()

queryset = session.query(length_table).filter(
    extract('year', length_table.c.timer) == year).all()


def get_moneies_list(table, asset, year, month, date):
    money_dict = {}
    for i in range(24):
        queryset = session.query(length_table).filter_by(pair=asset).filter(
            extract('year', length_table.c.timer) == year, extract(
                'month', length_table.c.timer) == month, extract('day', length_table.c.timer) == date, extract('hour', length_table.c.timer) == 10).all()

        queryset = models.ValuesLen.objects.filter(
            pair=asset, timer__year=year, timer__month=month, timer__day=date, timer__hour=i, ignore=False).values("money").order_by('timer')
        money_list = [record['money'] for record in queryset.values()]
        money_dict[i] = money_list
    return money_dict


assets = [
    "AUDUSD", "AUDCAD", "USDCHF", "EURNOK", "AUDNZD", "GBPJPY", "EURAUD", "AUDCHF", "GBPCHF",
    "GBPNZD", "EURGBP", "EURCAD", "EURNZD", "NZDCAD", "GBPCAD", "USDJPY", "NZDCHF", "USDNOK",
    "EURUSD", "NZDJPY", "CADJPY", "GBPUSD", "AUDJPY", "USDCAD", "EURJPY", "CADCHF", "USDJPY-OTC",
    "EURUSD-OTC", "EURGBP-OTC", "USDCHF-OTC", "EURJPY-OTC", "NZDUSD-OTC", "AUDCAD-OTC",
    "GBPUSD-OTC", "EURRUB-OTC", "USDRUB-OTC", "GBPJPY-OTC"
]

engine = create_engine(os.environ.get('sqlalchemy_uri'))
connection = engine.connect()
metadata = MetaData()
my_table = Table("boanapp_values", metadata, autoload_with=engine)

Session = sessionmaker(bind=engine)
session = Session()
all_dates = get_all_dates(my_table)

total_profit_dict = {}
for asset in assets:
    daily_profit_dict = {}
    for date in all_dates:
        hours = logic.get_moneies_list(
            asset, date.split('/')[2], date.split('/')[0], date.split('/')[1])
        dips = 0
        for hour in hours:
            profit = labouchere.ProphetC().get_profit(hours[hour])
            if profit < 0:
                dips += 1
            daily_profit_dict[date] = dips

    total_profit_dict[asset] = daily_profit_dict
x = {'AUDUSD': {'07/22/2019': 3, '07/23/2019': 8, '07/24/2019': 7, '07/25/2019': 7, '07/26/2019': 3},
     'AUDCAD': {'07/22/2019': 6, '07/23/2019': 8, '07/24/2019': 6, '07/25/2019': 7, '07/26/2019': 2}}

all_dates = pd.date_range(start=logic.get_last_date(),
                          end=logic.get_start_date()).strftime("%m/%d/%Y").to_list()

for asset in assets:
    try:
        print("Getting data for {}".format(asset))
        # query the table that has the data we need, and a specific asset
        y = session.query(my_table).filter_by(pair=asset)

        # read the sql object into a pandas data frame
        df = pd.read_sql(y.statement, y.session.bind)

        # sort, and convert the pandas object into a python dictionary
        df.sort_values(by="timer")
        # records_dict = df.to_dict("records")

        # calculate MA
        output = SMA(df, timeperiod=14, price="close")

        df["ma14"] = output
        # convert the dataframe into a python dictionary
        j = df.to_dict(orient="index")

        # calculate money for all the values
        for dic in j.values():
            if dic["open"] > dic["ma14"] and dic["greenred"] == 1:
                dic["money"] = 1
            elif dic["open"] < dic["ma14"] and dic["greenred"] == -1:
                dic["money"] = 1
            elif dic["greenred"] == 0:
                dic["money"] = 0
            else:
                dic["money"] = -1

        new_list = []
        for i in j.values():
            new_list.append(i)

        print("saving data for {}".format(asset))
        table2 = Table("boanapp_valuesma", metadata, autoload_with=engine)
        connection.execute(table2.insert(), new_list)
    except Exception as e:
        pass

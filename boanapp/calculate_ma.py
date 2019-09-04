import psycopg2
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
import pandas as pd
from talib import abstract
import os

assets = [
    "AUDUSD", "AUDCAD", "USDCHF", "EURNOK", "AUDNZD", "GBPJPY", "EURAUD", "AUDCHF", "GBPCHF",
    "GBPNZD", "EURGBP", "EURCAD", "EURNZD", "NZDCAD", "GBPCAD", "USDJPY", "NZDCHF", "USDNOK",
    "EURUSD", "NZDJPY", "CADJPY", "GBPUSD", "AUDJPY", "USDCAD", "EURJPY", "CADCHF", "USDJPY-OTC",
    "EURUSD-OTC", "EURGBP-OTC", "USDCHF-OTC", "EURJPY-OTC", "NZDUSD-OTC", "AUDCAD-OTC",
    "GBPUSD-OTC", "EURRUB-OTC", "USDRUB-OTC", "GBPJPY-OTC"
]

# instantiate SMA
# SMA = abstract.SMA

# calculate SMA

engine = create_engine(os.environ.get('sqlalchemy_uri'))
connection = engine.connect()
metadata = MetaData()
# my_table = Table("boanapp_values", metadata, autoload_with=engine)

Session = sessionmaker(bind=engine)
session = Session()

# for asset in assets:
#     try:
#         print("Getting data for {}".format(asset))
#         # query the table that has the data we need, and a specific asset
#         y = session.query(my_table).filter_by(pair=asset)

#         # read the sql object into a pandas data frame
#         df = pd.read_sql(y.statement, y.session.bind)

#         # sort, and convert the pandas object into a python dictionary
#         df.sort_values(by="timer")
#         # records_dict = df.to_dict("records")

#         # calculate MA
#         output = SMA(df, timeperiod=14, price="close")

#         df["ma14"] = output
#         # convert the dataframe into a python dictionary
#         j = df.to_dict(orient="index")

#         # calculate money for all the values
#         for dic in j.values():
#             if dic["open"] > dic["ma14"] and dic["greenred"] == 1:
#                 dic["money"] = 1
#             elif dic["open"] < dic["ma14"] and dic["greenred"] == -1:
#                 dic["money"] = 1
#             elif dic["greenred"] == 0:
#                 dic["money"] = 0
#             else:
#                 dic["money"] = -1

#         new_list = []
#         for i in j.values():
#             new_list.append(i)

#         print("saving data for {}".format(asset))
#         table2 = Table("boanapp_valuesma", metadata, autoload_with=engine)
#         connection.execute(table2.insert(), new_list)
#     except Exception as e:
#         pass

length_table = Table("boanapp_valuesma", metadata, autoload_with=engine)
for asset in assets:
    try:
        print("Getting data for {}".format(asset))
        # query the table that has the data we need, and a specific asset
        y2 = session.query(length_table).filter_by(pair=asset)

        # read the sql object into a pandas data frame
        df2 = pd.read_sql(y2.statement, y2.session.bind)

        # sort, and convert the pandas object into a python dictionary
        df2.sort_values(by="timer")

        j2 = df2.to_dict(orient="index")

        # find length of candles, and if MA is in them
        for dic in j2.values():
            if dic["min"] < dic["ma14"] < dic["max"]:
                dic["ignore"] = True
            else:
                dic["ignore"] = False

        new_list = []
        for i in j2.values():
            new_list.append(i)

        print("saving data for {}".format(asset))
        table2 = Table("boanapp_valueslen", metadata, autoload_with=engine)
        connection.execute(table2.insert(), new_list)
    except Exception as e:
        pass
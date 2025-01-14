#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import asyncio
import datetime
import logging
import os
import sys
import toml
import akshare as ak
import pandas as pd
from sqlalchemy import create_engine, text

NAME = os.path.basename(os.path.splitext(__file__)[0])
CONFIG = toml.load(os.getenv('ENV', 'development') + '.toml')
job_filename = os.path.splitext(os.path.basename(__file__))[0]
logging.basicConfig(format=CONFIG['default']['log_format'], level=getattr(logging, CONFIG['default']['log_level'].upper()), filename=f'{job_filename}.log')
DATABASE_URL = 'mysql+pymysql://%(user)s:%(password)s@%(host)s:%(port)d/%(db)s?charset=%(charset)s' % CONFIG['pymysql']
engine = create_engine(DATABASE_URL)
MYCONFIG = CONFIG['job'][job_filename]

def get_daily_data(day_start, day_end, symbol):
    start_date = datetime.datetime.strptime(day_start,'%Y-%m-%d').strftime("%Y%m%d")
    end_date = datetime.datetime.strptime(day_end,'%Y-%m-%d').strftime("%Y%m%d")
    df = ak.stock_zh_index_daily_em(symbol=symbol, start_date=start_date, end_date=end_date)
    df['symbol'] = symbol
    with engine.connect() as connection:
        for index, row in df.iterrows():
            insert_stmt = """INSERT INTO smart_investment.a_stock_index_daily_data 
            (`date`, symbol, open, close, high, low, volume, amount) 
            VALUES (:date, :symbol, :open, :close, :high, :low, :volume, :amount) 
            ON DUPLICATE KEY UPDATE 
            open = VALUES(open), 
            close = VALUES(close), 
            high = VALUES(high), 
            low = VALUES(low), 
            volume = VALUES(volume), 
            amount = VALUES(amount)
            """
            connection.execute(text(insert_stmt), row.to_dict())
        connection.commit()
        connection.close()


def main():
    """
    默认更新 最近7日数据

    更新全量数据
    python cron/update_a_stock_index_daily_data.py '2014-01-01'
    """
    day_end = datetime.datetime.today() 
    day_start = datetime.datetime.today() - datetime.timedelta(days=8)
    day_start = day_start.strftime("%Y-%m-%d")
    day_end = day_end.strftime("%Y-%m-%d")
    if len(sys.argv) > 1 and sys.argv[1]:
        day_start = sys.argv[1]
    if len(sys.argv) > 2 and sys.argv[2]:
        day_end = sys.argv[2]
    for symbol in MYCONFIG['symbols']:
        print(f'getting daily data {symbol} {day_start} => {day_end}')
        get_daily_data(day_start,day_end,symbol)



if __name__ == "__main__":
    main()

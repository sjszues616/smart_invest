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
from sqlalchemy import create_engine

NAME = os.path.basename(os.path.splitext(__file__)[0])
CONFIG = toml.load(os.getenv('ENV', 'development') + '.toml')
job_filename = os.path.splitext(os.path.basename(__file__))[0]
logging.basicConfig(format=CONFIG['default']['log_format'], level=getattr(logging, CONFIG['default']['log_level'].upper()), filename=f'{job_filename}.log')
DATABASE_URL = 'mysql+pymysql://%(user)s:%(password)s@%(host)s:%(port)d/%(db)s?charset=%(charset)s' % CONFIG['pymysql']
engine = create_engine(DATABASE_URL)
MYCONFIG = CONFIG['job'][job_filename]

def get_daily_data(day_start, day_end):
    # sz001696 宗申动力
    # 沪深300 上海交易所 000300 深圳交易所 399300
    # 科创50 000688
    symbol = '000300'
    today = datetime.datetime.today()
    start_date = (today-datetime.timedelta(days=90)).strftime("%Y%m%d")
    end_date = today.strftime("%Y%m%d")
    df = ak.stock_zh_index_daily_em(symbol=f'sh{symbol}', start_date=start_date, end_date=end_date)
    df['date'] = pd.to_datetime(df['date'])
    df['symbol'] = symbol
    df.to_sql(MYCONFIG['table_name'], con=engine, if_exists='replace', index=False)


def main():
    day_end = datetime.datetime.today().replace(day=1) - datetime.timedelta(days=1)
    day_start = (datetime.datetime.today().replace(day=1) - datetime.timedelta(days=1)).replace(day=1)
    day_start = day_start.strftime("%Y-%m-%d")
    day_end = day_end.strftime("%Y-%m-%d")
    if len(sys.argv) > 1 and sys.argv[1]:
        day_start = sys.argv[1]
    if len(sys.argv) > 2 and sys.argv[2]:
        day_end = sys.argv[2]
    get_daily_data(day_start,day_end)


if __name__ == "__main__":
    main()

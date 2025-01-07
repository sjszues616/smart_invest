#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import asyncio
import datetime
import logging
import os
import sys
import toml
import akshare as ak
import records
import pandas as pd

NAME = os.path.basename(os.path.splitext(__file__)[0])
CONFIG = toml.load(os.getenv('ENV', 'development') + '.toml')
logger_filename = os.path.splitext(os.path.basename(__file__))[0]
logging.basicConfig(format=CONFIG['default']['log_format'], level=getattr(logging, CONFIG['default']['log_level'].upper()), filename=f'{logger_filename}.log')
DATABASE_URL = 'mysql+pymysql://%(user)s:%(password)s@%(host)s:%(port)d/%(db)s?charset=%(charset)s' % CONFIG['pymysql']
database = records.Database(DATABASE_URL, echo=True, pool_pre_ping=True, pool_recycle=60, pool_timeout=30)

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
    logging.info(f'sql: {sql}')
    results = clickhouse_client.execute(sql)
    res = []

    for v in results:
        res.append({
            'month': v[0].strftime("%Y-%m"),
            'cost': round(float(v[1]),4),
            'revenue': round(float(v[2]),4),
            'gp': round(float(v[2]-v[1]),4),
        })
    logging.info(f'count={len(res)}; res: {res}')
    # print(f'count={len(res)}; res: {res}')
    return res


def main():
    app_token = CONFIG['job']['update_bi_feishu_table']['app_token']
    table_id = CONFIG['job']['update_bi_feishu_table']['table_id']
    day_end = datetime.datetime.today().replace(day=1) - datetime.timedelta(days=1)
    day_start = (datetime.datetime.today().replace(day=1) - datetime.timedelta(days=1)).replace(day=1)

    day_start = day_start.strftime("%Y-%m-%d")
    day_end = day_end.strftime("%Y-%m-%d")

    if len(sys.argv) > 1 and sys.argv[1]:
        day_start = sys.argv[1]
    if len(sys.argv) > 2 and sys.argv[2]:
        day_end = sys.argv[2]
    
    month_data = get_month_data(day_start, day_end)
    feishu_alert = FeiShuAlert()
    feishu_alert._insert_records(app_token, table_id, month_data)

if __name__ == "__main__":
    main()

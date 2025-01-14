import datetime
import os
import sys
from sqlalchemy import create_engine
import toml
import pandas as pd

from utils import gen_stock_candle_trend_chart

CONFIG = toml.load(os.getenv('ENV', 'development') + '.toml')
DATABASE_URL = 'mysql+pymysql://%(user)s:%(password)s@%(host)s:%(port)d/%(db)s?charset=%(charset)s' % CONFIG['pymysql']
engine = create_engine(DATABASE_URL)

def get_data(table, symbol, day_start, day_end) -> pd.DataFrame:
    ''' 获取最近120天的交易数据
    '''
    day_start = (datetime.datetime.strptime(day_start,'%Y-%m-%d') - datetime.timedelta(days=60)).strftime('%Y-%m-%d')
    query = f"SELECT * FROM {table} WHERE date > '{day_start}' and date < '{day_end}' and symbol='{symbol}'"
    df = pd.read_sql_query(query, con=engine)
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    return df


def main(table, symbol, day_start, day_end):
    '''根据指定指数60日线一下,终止任何交易, 等待指数回调到指定区间后,进行左侧交易
    '''
    df = get_data(table, symbol, day_start, day_end)
    filename = os.path.join('wwwroot',f'{table}_{symbol}_{day_start}_{day_end}.png')
    gen_stock_candle_trend_chart(df,filename)

if __name__ == '__main__':
    symbol='sh000300'
    table = 'a_stock_index_daily_data'
    day_end = datetime.datetime.today()
    day_start = datetime.datetime.today() - datetime.timedelta(days=180)
    day_start = day_start.strftime('%Y-%m-%d')
    day_end = day_end.strftime('%Y-%m-%d')

    if len(sys.argv) > 1 and sys.argv[1]:
        table = sys.argv[1]
    if len(sys.argv) > 2 and sys.argv[2]:
        symbol = sys.argv[2]
    main(table, symbol, day_start, day_end)    
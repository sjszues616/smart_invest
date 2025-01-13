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

def get_data(symbol) -> pd.DataFrame:
    ''' 获取最近120天的交易数据
    '''
    today = datetime.datetime.today()
    date_start = (today - datetime.timedelta(days=120)).strftime('%Y-%m-%d')
    date_end = today.strftime('%Y-%m-%d')
    query = f"SELECT * FROM a_stock_daily_data WHERE date > '{date_start}' and date < '{date_end}' and symbol='{symbol}'"
    df = pd.read_sql_query(query, con=engine)
    df.set_index('date', inplace=True)
    return df


def main(symbol):
    '''根据指定指数60日线一下,终止任何交易, 等待指数回调到指定区间后,进行左侧交易
    '''
    df = get_data(symbol)
    filename = os.path.join('wwwroot',f'alert_a_stock_close_trade_{datetime.datetime.today().strftime("%Y%m%d")}.png')
    gen_stock_candle_trend_chart(df,filename)

if __name__ == '__main__':
    symbol='sh000300'
    if len(sys.argv) > 1 and sys.argv[1]:
        symbol = sys.argv[1]
    main(symbol)
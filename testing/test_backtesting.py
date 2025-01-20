import datetime
import sys
from backtesting import Backtest, Strategy
from backtesting.lib import crossover 
import numpy as np
from sqlalchemy import create_engine
from backtesting.test import SMA, GOOG
import pandas as pd
from bokeh.io import save

DATABASE_URL = 'mysql+pymysql://kevin:4jikQ7PPtU@127.0.0.1:3306/smart_investment?charset=utf8mb4' 
engine = create_engine(DATABASE_URL)

def calculate_bollinger_bands(series, window=20, num_std=2):
    # 手动计算滚动均值和标准差
    ma = np.array([series[i-window:i].mean() for i in range(window, len(series))])
    std = np.array([series[i-window:i].std() for i in range(window, len(series))])
    upper = ma + (std * num_std)
    lower = ma - (std * num_std)
    # 填充前 window 个值为 NaN
    ma = np.concatenate([np.full(window, np.nan), ma])
    upper = np.concatenate([np.full(window, np.nan), upper])
    lower = np.concatenate([np.full(window, np.nan), lower])
    return upper, lower, ma

class BollingerBandsStrategy(Strategy):
    def init(self):
        # 计算布林带
        self.upper, self.lower, self.ma = self.I(calculate_bollinger_bands, self.data.Close, window=20, num_std=2)

    def next(self):
        # 布林带交易逻辑
        if len(self.data.Close) < 20:  # 确保有足够的数据
            return
        if self.data.Close[-1] > self.upper[-1]:  # 价格突破上轨，卖出
            self.sell()
        elif self.data.Close[-1] < self.lower[-1]:  # 价格突破下轨，买入
            self.buy()

class SmaCross(Strategy):
    def init(self):
        price = self.data.Close
        self.ma1 = self.I(SMA, price, 10)
        self.ma2 = self.I(SMA, price, 20)

    def next(self):
        if crossover(self.ma1, self.ma2):
            self.buy()
        elif crossover(self.ma2, self.ma1):
            self.sell()

def get_data(table, symbol, day_start, day_end) -> pd.DataFrame:
    ''' 获取最近120天的交易数据
    '''
    day_start = (datetime.datetime.strptime(day_start,'%Y-%m-%d') - datetime.timedelta(days=60)).strftime('%Y-%m-%d')
    query = f"SELECT * FROM {table} WHERE date > '{day_start}' and date < '{day_end}' and symbol='{symbol}'"
    df = pd.read_sql_query(query, con=engine)
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    df.rename(columns={
    'open': 'Open',
    'high': 'High', 
    'low': 'Low', 
    'close': 'Close', 
    'volume': 'Volume'}, inplace=True)
    # print(df)
    return df

def main(table, symbol, day_start, day_end):
    df = get_data(table, symbol, day_start, day_end)
    bt = Backtest(df, BollingerBandsStrategy, commission=.002,
              exclusive_orders=True)
    stats = bt.run()    # 自定义 Bokeh 格式化
    print(stats)
    save(bt.plot(),filename='backtest_BollingerBands.html')


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
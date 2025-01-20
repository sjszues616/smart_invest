
'''
Author: Charmve yidazhang1@gmail.com
Date: 2023-03-23 15:07:38
LastEditors: Charmve yidazhang1@gmail.com
LastEditTime: 2023-03-24 02:42:20
FilePath: /Qbot/qbot/qbot.py
Version: 1.0.1
Blogs: charmve.blog.csdn.net
GitHub: https://github.com/Charmve
Description: 

Copyright (c) 2023 by Charmve, All Rights Reserved. 
Licensed under the MIT License.
'''

import datetime
import pandas as pd
import numpy as np
import time


from sqlalchemy import create_engine

# 设置股票代码和起止日期
# code = '600000.SH'
code = '601318'
start_date = '20230320'
end_date = time.strftime('%Y%m%d',time.localtime(time.time()))


def get_data(engine, table, symbol, day_start, day_end) -> pd.DataFrame:
    ''' 获取最近120天的交易数据
    '''
    day_start = (datetime.datetime.strptime(day_start,'%Y-%m-%d') - datetime.timedelta(days=60)).strftime('%Y-%m-%d')
    query = f"SELECT * FROM {table} WHERE date > '{day_start}' and date < '{day_end}' and symbol='{symbol}'"
    df = pd.read_sql_query(query, con=engine)
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    return df

# 从tushare获取股票数据
# data = ts.get_k_data(code, start=start_date, end=end_date)
# print(data)
def process(data):
    # 计算均线、BIAS和BOLL指标

    # 假设 data 是包含 'close', 'high', 'low' 列的 DataFrame
    # 计算移动平均线
    data['ma5'] = data['close'].rolling(window=5, min_periods=1).mean()
    data['ma10'] = data['close'].rolling(window=10, min_periods=1).mean()
    data['ma20'] = data['close'].rolling(window=20, min_periods=1).mean()

    # 计算乖离率
    data['bias1'] = (data['close'] - data['ma5']) / data['ma5'] * 100
    data['bias2'] = (data['close'] - data['ma10']) / data['ma10'] * 100
    data['bias3'] = (data['close'] - data['ma20']) / data['ma20'] * 100

    # 计算布林带
    data['middle'] = data['close'].rolling(window=20, min_periods=1).mean()  # 中轨
    data['std'] = data['close'].rolling(window=20, min_periods=1).std()     # 标准差
    data['upper'] = data['middle'] + 2 * data['std']                        # 上轨
    data['lower'] = data['middle'] - 2 * data['std']                        # 下轨

    # 计算随机指标
    low_min = data['low'].rolling(window=9, min_periods=1).min()  # 9 日内最低价
    high_max = data['high'].rolling(window=9, min_periods=1).max()  # 9 日内最高价
    data['k'] = (data['close'] - low_min) / (high_max - low_min) * 100  # K 值
    data['d'] = data['k'].rolling(window=3, min_periods=1).mean()  # D 值（K 值的 3 日移动平均）

    # 计算 RSI
    delta = data['close'].diff()  # 价格变化
    gain = (delta.where(delta > 0, 0)).rolling(window=14, min_periods=1).mean()  # 平均上涨幅度
    loss = (-delta.where(delta < 0, 0)).rolling(window=14, min_periods=1).mean()  # 平均下跌幅度
    rs = gain / loss  # RS 值
    data['rsi'] = 100 - (100 / (1 + rs))  # RSI


    # 初始化买卖信号
    signals = np.zeros(len(data))

    # 第一个策略：均线和BIAS指标信号
    condition1 = (data['ma5'] > data['ma10']) & (data['ma5'] > data['ma20']) & (data['bias1'] > data['bias2']) & (data['bias1'] > data['bias3'])
    signals += 0.2 * condition1.astype(int)

    # 第二个策略：股价低于BOLL线底
    condition2 = (data['close'] < data['lower'])
    signals += 0.3 * condition2.astype(int)

    # 第三个策略：K线上穿D线
    condition3 = (data['k'] > data['d']) & (data['k'].shift() < data['d'].shift())
    signals += 0.2 * condition3.astype(int)

    # 第四个策略：RSI指标信号
    condition4 = (data['rsi'] > 80) | (data['rsi'] < 20)
    signals += 0.3 * condition4.astype(int)

    print("signals: ", signals.tail(20))

    # 根据信号生成交易指令，并计算收益率
    orders = np.zeros_like(signals)
    orders[signals > 0] = 1   # 买入信号
    orders[signals < 0] = -1  # 卖出信号
    returns = np.diff(data['close']) * orders[:-1]

    # 输出结果
    print('Total returns:', returns.sum())
    print('Positive trades:', len(returns[returns > 0]))
    print('Negative trades:', len(returns[returns < 0]))

def main():
    DATABASE_URL = 'mysql+pymysql://kevin:4jikQ7PPtU@127.0.0.1:3306/smart_investment?charset=utf8mb4' 
    engine = create_engine(DATABASE_URL)
    symbol='sh000300'
    symbol='001696'
    table = 'a_stock_stock_daily_data'
    day_end = datetime.datetime.today()
    day_start = datetime.datetime.today() - datetime.timedelta(days=180)
    day_start = day_start.strftime('%Y-%m-%d')
    day_end = day_end.strftime('%Y-%m-%d')
    # 示例数据：假设 df 是包含日期、开盘价、收盘价等数据的 DataFrame
    df = get_data(engine, table, symbol, day_start, day_end)
    print(df)
    process(df)

if __name__ == '__main__':
    main()
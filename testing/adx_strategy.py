'''
Author: Charmve yidazhang1@gmail.com
Date: 2023-03-18 18:06:06
LastEditors: Charmve yidazhang1@gmail.com
LastEditTime: 2023-03-18 18:14:39
FilePath: /Qbot/qbot/strategies/adx_strategy.py
Version: 1.0.1
Blogs: charmve.blog.csdn.net
GitHub: https://github.com/Charmve
Description: 获取股票数据并进行量化回测——基于ADX和MACD趋势策略

https://blog.csdn.net/ndhtou222/article/details/121219649

Copyright (c) 2023 by Charmve, All Rights Reserved. 
Licensed under the MIT License.
'''
import quantstats as qs
import datetime
import pandas as pd  
import numpy as np
import matplotlib.pyplot as plt
import pyfolio as pf
from sqlalchemy import create_engine


def adx_strategy(df,ma1=13,ma2=55,ma3=89,adx=25):
    #计算MACD和ADX指标
    df['EMA1'] = df['close'].ewm(span=ma1, adjust=False).mean()
    df['EMA2'] = df['close'].ewm(span=ma2, adjust=False).mean()
    df['EMA3'] = df['close'].ewm(span=ma3, adjust=False).mean()
    
    # 计算快速 EMA (12 日 EMA)
    df['EMA12'] = df['close'].ewm(span=12, adjust=False).mean()
    # 计算慢速 EMA (26 日 EMA)
    df['EMA26'] = df['close'].ewm(span=26, adjust=False).mean()
    # 计算 MACD 线
    df['MACD'] = df['EMA12'] - df['EMA26']
    # 计算信号线 (MACD 的 9 日 EMA)
    df['MACDSignal'] = df['MACD'].ewm(span=9, adjust=False).mean()
    # 计算 MACD 直方图
    df['MACDHist'] = df['MACD'] - df['MACDSignal']

    # 计算 ADX
    df['High-Low'] = df['high'] - df['low']
    df['High-PrevClose'] = abs(df['high'] - df['close'].shift(1))
    df['Low-PrevClose'] = abs(df['low'] - df['close'].shift(1))
    df['TR'] = df[['High-Low', 'High-PrevClose', 'Low-PrevClose']].max(axis=1)

    df['High-PrevHigh'] = df['high'] - df['high'].shift(1)
    df['Low-PrevLow'] = df['low'].shift(1) - df['low']
    df['+DM'] = df.apply(lambda x: x['High-PrevHigh'] if x['High-PrevHigh'] > x['Low-PrevLow'] and x['High-PrevHigh'] > 0 else 0, axis=1)
    df['-DM'] = df.apply(lambda x: x['Low-PrevLow'] if x['Low-PrevLow'] > x['High-PrevHigh'] and x['Low-PrevLow'] > 0 else 0, axis=1)

    window = 14
    df['TR_smooth'] = df['TR'].rolling(window=window, min_periods=1).sum()
    df['+DM_smooth'] = df['+DM'].rolling(window=window, min_periods=1).sum()
    df['-DM_smooth'] = df['-DM'].rolling(window=window, min_periods=1).sum()

    df['+DI'] = (df['+DM_smooth'] / df['TR_smooth']) * 100
    df['-DI'] = (df['-DM_smooth'] / df['TR_smooth']) * 100

    df['DX'] = (abs(df['+DI'] - df['-DI']) / (df['+DI'] + df['-DI'])) * 100
    df['ADX'] = df['DX'].rolling(window=window, min_periods=1).mean()

    #设计买卖信号:21日均线大于42日均线且42日均线大于63日均线;ADX大于前值小于25；MACD大于前值
    df['Buy_Sig'] =(df['EMA1']>df['EMA2'])&(df['EMA2']>df['EMA3'])&(df['ADX']<=adx)\
                    &(df['ADX']>df['ADX'].shift(1))&(df['MACDHist']>df['MACDHist'].shift(1))
    df.loc[df.Buy_Sig,'Buy_Trade'] = 1
    df.loc[df.Buy_Trade.shift(1)==1,'Buy_Trade'] = " "
    #避免最后三天内出现交易
    df.Buy_Trade.iloc[-3:]  = " " 
    df.loc[df.Buy_Trade==1,'Buy_Price'] = df.close
    df.Buy_Price = df.Buy_Price.ffill()
    df['Buy_Daily_Return']= (df.close - df.Buy_Price)/df.Buy_Price
    df.loc[df.Buy_Trade.shift(3)==1,'Sell_Trade'] = -1
    df.loc[df.Sell_Trade==-1,'Buy_Total_Return'] = df.Buy_Daily_Return
    df.loc[(df.Sell_Trade==-1)&(df.Buy_Daily_Return==0),'Buy_Total_Return'] = \
                                (df.Buy_Price - df.Buy_Price.shift(1))/df.Buy_Price.shift(1)
    df.loc[(df.Sell_Trade==-1)&(df.Buy_Trade.shift(1)==1),'Buy_Total_Return'] = \
                                (df.close-df.Buy_Price.shift(2))/df.Buy_Price.shift(2)
    #返回策略的日收益率
    return df.Buy_Total_Return.fillna(0)



def get_data(engine, table, symbol, day_start, day_end) -> pd.DataFrame:
    ''' 获取最近120天的交易数据
    '''
    day_start = (datetime.datetime.strptime(day_start,'%Y-%m-%d') - datetime.timedelta(days=60)).strftime('%Y-%m-%d')
    query = f"SELECT * FROM {table} WHERE date > '{day_start}' and date < '{day_end}' and symbol='{symbol}'"
    df = pd.read_sql_query(query, con=engine)
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    return df


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
    # df1 = adx_strategy(df)

    # df.close.plot(figsize=(12,6))
    plt.title('神州泰岳股价走势\n2010-2021',size=15)
    # qs.reports.html(df.close.pct_change(), output='report.html')
    # qs.reports.html(adx_strategy(df), output='report2.html')

if __name__ == '__main__':
    main()
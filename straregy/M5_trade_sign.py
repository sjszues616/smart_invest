import datetime
import pandas as pd
import mplfinance as mpf
import akshare as ak
from sqlalchemy import create_engine


def gen_stock_candle_trend_chart(df:pd.DataFrame):
    # dimensiona & measure & target    
    measure_name = 'custom_measure_MA5'

    # dimensiona 用于计算交易信号
    df[measure_name] = df['close'].rolling(window=5).mean()
    # 数据整理
    
    # 生成交易信号 交易策略#####
    df['signal'] = 0  # 初始化信号列
    df['position'] = 0
    df['ma_up'] = df[measure_name].diff() > 0 # 均线上升为 True，下降为 False
    df = df.dropna()
    print(df.astype)


    df.loc[df['ma_up'] & df['ma_up'].shift(1) != True, 'signal'] = 1  # MA5 上升 上升区间
    df.loc[df['ma_up'] != True & df['ma_up'].shift(1), 'signal'] = -1  # MA5 下降 下降区间
    # 当 signal 为 1 或前一天的 position 大于 0 时，position 为 1
    df.loc[(df['signal'] == 1) | (df['position'].shift(1) > 0), 'position'] = 1

    # 当 signal 为 -1 或前一天的 position 大于 0 时，position 为 0
    df.loc[(df['signal'] == -1) | (df['position'].shift(1) > 0), 'position'] = 0

    # 计算每日收益率
    df['returns'] = df['close'].pct_change()
    # 计算策略收益率
    df['strategy_returns'] = df['position']   * df['returns']
    # 计算累计收益率 cumprod() 复利累计收益
    df['cumulative_returns'] = (1 + df['strategy_returns']).cumprod()
    # 可视化结果
    import matplotlib.pyplot as plt

    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['cumulative_returns'], label='Strategy Returns')
    plt.plot(df.index, (1 + df['returns']).cumprod(), label='Market Returns')
    plt.title('Backtest Results')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Returns')
    plt.legend()
    plt.savefig('xxxx.png')

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
    table = 'a_stock_index_daily_data'
    day_end = datetime.datetime.today()
    day_start = datetime.datetime.today() - datetime.timedelta(days=180)
    day_start = day_start.strftime('%Y-%m-%d')
    day_end = day_end.strftime('%Y-%m-%d')
    # 示例数据：假设 df 是包含日期、开盘价、收盘价等数据的 DataFrame
    df = get_data(engine, table, symbol, day_start, day_end)
    gen_stock_candle_trend_chart(df)

if __name__ == '__main__':
    main()
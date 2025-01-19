import pandas as pd
import mplfinance as mpf
import akshare as ak


def gen_stock_candle_trend_chart(df:pd.DataFrame):
    # dimensiona & measure & target    
    measure_name = 'custom_measure_MA5'

    # dimensiona 用于计算交易信号
    df[measure_name] = df['close'].rolling(window=5).mean()

    # 生成交易信号
    df['signal'] = 0  # 初始化信号列

    df_cleaned = df.dropna()



def main():
    pass

if __name__ == '__main__':
    main()
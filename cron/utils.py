import pandas as pd
import mplfinance as mpf

def gen_stock_candle_trend_chart(df:pd.DataFrame,filename:str):
    
    mc = mpf.make_marketcolors(alpha=0.9,up='#EB6050',down='#6CA585',inherit=True)
    s = mpf.make_mpf_style(base_mpf_style='tradingview',marketcolors=mc)
    # moving average mav 均线
    # volume 是否显示交易量
    # 

    df['MA5'] = df['close'].rolling(window=5).mean()
    df['MA10'] = df['close'].rolling(window=10).mean()
    df['MA20'] = df['close'].rolling(window=20).mean()
    df['MA60'] = df['close'].rolling(window=60).mean()
    df_cleaned = df.dropna()
    df_recent = df_cleaned[-60:]
    ap = [
        mpf.make_addplot(df_recent['MA5'], color='black', label='MA5'),
        mpf.make_addplot(df_recent['MA10'], color='#C2602E', label='MA10'),
        mpf.make_addplot(df_recent['MA20'], color='#D9649F', label='MA20'),
        mpf.make_addplot(df_recent['MA60'], color='green', label='MA60')
    ]
    plot_params = {
        "addplot":ap,
        "savefig": filename
    }

    fig, axes =mpf.plot(df_recent, 
            type='candle', 
            volume=True, 
            returnfig=True,
            style=s, 
            title='Index stock candle trend chart', 
            ylabel='price', 
            ylabel_lower='trading volume',
            figscale=1,**plot_params)
    
    axes[0].legend()
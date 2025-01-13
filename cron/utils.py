import pandas as pd
import mplfinance as mpf

def gen_stock_candle_trend_chart(df:pd.DataFrame,filename:str):
    
    mc = mpf.make_marketcolors(alpha=0.9,up='#EB6050',down='#6CA585',inherit=True)
    s = mpf.make_mpf_style(base_mpf_style='tradingview',marketcolors=mc)
    # moving average mav 均线
    # volume 是否显示交易量
    # 
    plot_params = {
        "mav": (5,10,20,60),
        "savefig": filename
    }
    mpf.plot(df, 
            type='candle', 
            volume=True, 
            style=s, 
            title='Index stock candle trend chart', 
            ylabel='price', 
            ylabel_lower='trading volume',
            figscale=1,**plot_params)
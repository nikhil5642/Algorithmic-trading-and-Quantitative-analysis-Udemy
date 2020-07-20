from stocktrends import Renko
from algotrade.indicators import get_ATR

def renko_dataframe(DF):
    df=DF.copy()
    df.reset_index(inplace=True)
    df=df.loc[:,["Date","Open","High","Low","Close","Volume"]]
    df.columns = ["date","open","high","low","close","volume"]
    renko_df=Renko(df)
    renko_df.brick_size=round(get_ATR(DF,120)["ATR"][-1],0)
    df2=renko_df.get_ohlc_data()
    return df2
    

def add_renko_dataframe(DF):
    renko_df=renko_dataframe(DF)
    DF["renko_open"]=renko_df["open"]
    DF["renko_high"]=renko_df["high"]
    DF["renko_low"]=renko_df["low"]
    DF["renko_close"]=renko_df["close"]
    DF["renko_uptrend"]=renko_df["uptrend"]
    

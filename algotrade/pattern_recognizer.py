import talib 

def CDL3INSIDE(df):
    talib.CDL3INSIDE(df["Open"],df["High"],df["Low"],df["Adj Close"])
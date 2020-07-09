import plotly.graph_objs as go

def plotCandleStick(df):
    return go.Candlestick(x=df.index, open=df.Open,close=df.Close,high=df.High,low=df.Low,name="CandleStick Chart")
    

def plotMA(df,n,colour):
    return go.Scatter(x=df.index,y=df.Close.rolling(n).mean(),line=dict(color=colour, width=1),name="SMA "+str(n),)




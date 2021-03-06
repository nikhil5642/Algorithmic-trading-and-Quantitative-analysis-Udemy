import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from algotrade.plotter import plotCandleStick,plotMA
from algotrade.indicators import add_MACD,add_ATR,add_BollBnd,add_RSI,add_ADX,add_OBV
from algotrade.slope import add_slope
from algotrade.renko import add_renko_dataframe
import plotly.graph_objs as go
from algotrade.performance_measurement import CAGR
from algotrade.stock_universe import nifty50
stocks=["ITC.NS","RELIANCE.NS"]

cl_price=pd.DataFrame()
complete_data={}
# for ticker in stocks:
#     cl_price[ticker]=yf.download(ticker,period="max",interval="1d")["Adj Close"]
# for ticker in stocks:
#     complete_data[ticker]=yf.download(ticker,period="max",interval="1d")
# cl_standardized=(cl_price-cl_price.mean())/cl_price.std()
# cl_standardized.plot()
# plt.show()

data=yf.download("ITC.NS",period="max",interval="1d")

add_MACD(data)
add_ATR(data,20)
add_BollBnd(data,20)
add_RSI(data,14)
add_ADX(data,14)
add_OBV(data)
add_slope(data,20)
add_renko_dataframe(data)

print(CAGR(data))
layout = dict(
            title="ITC",
            xaxis = dict(
                type="category",
                categoryorder='category ascending')
                )
go.Figure(data=[plotCandleStick(data),plotMA(data,10,"blue"),plotMA(data,20,"red")],
            layout=layout).show()


print(data)
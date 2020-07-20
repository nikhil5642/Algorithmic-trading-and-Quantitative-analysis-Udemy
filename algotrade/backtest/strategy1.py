import yfinance as yf
from algotrade.stock_universe import nifty50
from algotrade.performance_measurement import CAGR,volatility,sharpe,max_dd


data=yf.download("ITC.NS",interval="1mo",duration = "max")
data["mon_ret"]=data["Close"].pct_change()
print(CAGR(data,monthly=True))
print(sharpe(data,0.025,monthly=True))
print(max_dd(data))


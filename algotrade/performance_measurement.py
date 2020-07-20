import numpy as np
def CAGR(DF,weekly=False,monthly=False,yearly=False):
    """CAGR calculation for daily data"""
    if yearly:
        x=1
    elif monthly:
        x=12
    elif weekly:
        x=52
    else:
        x=252
    df=DF.copy()
    df["ret"]=df["Close"].pct_change()
    df["cum_return"]=(1+df["ret"]).cumprod()
    n= len(df)/x # change it to 52 for weekly and 12 for monthly 
    cagr=(df["cum_return"][-1])**(1/n)-1
    return cagr
    
def volatility(DF,weekly=False,monthly=False,yearly=False):
    """Volatility calculation"""

    if yearly:
        x=1
    elif monthly:
        x=12
    elif weekly:
        x=52
    else:
        x=252
    df=DF.copy()
    df["ret"]=df["Close"].pct_change()
    vol=df["ret"].std()*np.sqrt(x)
    return vol

def sharpe(DF,rf,weekly=False,monthly=False,yearly=False):
    df=DF.copy()
    if weekly:
        sr=(CAGR(df,weekly=True)-rf)/volatility(df,weekly=True)
    elif monthly:
        sr=(CAGR(df,monthly=True)-rf)/volatility(df,monthly=True)
    elif yearly:
        sr=(CAGR(df,yearly=True)-rf)/volatility(df,yearly=True)
    else:
        sr=(CAGR(df)-rf)/volatility(df)
            
    return sr

def sortino(DF,rf,weekly=False,monthly=False,yearly=False):
    if yearly:
        x=1
    elif monthly:
        x=12
    elif weekly:
        x=52
    else:
        x=252
    df=DF.copy()
    df["ret"]=df["Close"].pct_change()
    neg_vol=df[df["ret"]<0]["ret"].std()*np.sqrt(x)

    if weekly:
        sr=(CAGR(df,weekly=True)-rf)/neg_vol
    elif monthly:
        sr=(CAGR(df,monthly=True)-rf)/neg_vol
    elif yearly:
        sr=(CAGR(df,yearly=True)-rf)/neg_vol
    else:
        sr=(CAGR(df)-rf)/neg_vol
    
    return sr
    
def max_dd(DF):
    df=DF.copy()
    df["ret"]=df["Close"].pct_change()
    df["cum_return"]=(1+df["ret"]).cumprod()
    df["cum_roll_max"]=df["cum_return"].cummax()
    df["drawdown"]=df["cum_roll_max"]-df["cum_return"]
    df["drawdown_pct"]=df["drawdown"]/df["cum_roll_max"]
    max_dd=df["drawdown"].max()
    return max_dd
    
def calmer(DF,weekly=False,monthly=False,yearly=False):
    df=DF.copy()
    if yearly:
        clmr=CAGR(df,yearly=True)/max_dd(df)
    elif monthly:
        clmr = CAGR(df,monthly=True)/max_dd(df)
    elif weekly:
        clmr=CAGR(df,weekly=True)/max_dd(df)
    else:
        clmr=CAGR(df)/max_dd(df)
    return clmr
    

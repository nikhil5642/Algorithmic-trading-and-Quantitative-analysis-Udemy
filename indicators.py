import numpy as np
def add_MACD(df,a=12,b=26,c=9):
    """function to calculate MACD
       typical values a = 12; b =26, c =9"""
    df["MACD"]=df["Adj Close"].ewm(span=a,min_periods=a).mean()-df["Adj Close"].ewm(span=b,min_periods=b).mean()
    df["Signal"]=df["MACD"].ewm(span=c,min_periods=c).mean()


    
def add_ATR(df,n):
    "function to calculate True Range and Average True Range"
    df['H-L']=abs(df['High']-df['Low'])
    df['H-PC']=abs(df['High']-df['Adj Close'].shift(1))
    df['L-PC']=abs(df['Low']-df['Adj Close'].shift(1))
    df['TR']=df[['H-L','H-PC','L-PC']].max(axis=1,skipna=False)
    df['ATR'] = df['TR'].rolling(n).mean()
    df.drop(['H-L','H-PC','L-PC'],axis=1,inplace=True)
    

def add_BollBnd(df,n):
    "function to calculate Bollinger Band"
    df["MA"] = df['Adj Close'].rolling(n).mean()
    df["BB_up"] = df["MA"] + 2*df['Adj Close'].rolling(n).std(ddof=0) #ddof=0 is required since we want to take the standard deviation of the population and not sample
    df["BB_dn"] = df["MA"] - 2*df['Adj Close'].rolling(n).std(ddof=0) #ddof=0 is required since we want to take the standard deviation of the population and not sample
    df["BB_width"] = df["BB_up"] - df["BB_dn"] 
    


def add_RSI(df,n):
   df["delta"]=df["Adj Close"]-df["Adj Close"].shift(1)
   df["gain"]=df["delta"].apply(lambda x: x if x>0 else 0)
   df["loss"]=df["delta"].apply(lambda x: abs(x) if x<0 else 0)
   avg_gain=[]
   avg_loss=[]
   for i in range(len(df)):
      if i<n:
         avg_gain.append(np.NaN)
         avg_loss.append(np.NaN)
      elif i==n:
         avg_gain.append(df["gain"].iloc[:n].mean())
         avg_loss.append(df["loss"].iloc[:n].mean())
      else:
         avg_gain.append(((n-1)*avg_gain[i-1]+df["gain"].iloc[i])/n)
         avg_loss.append(((n-1)*avg_loss[i-1]+df["loss"].iloc[i])/n)
               
   df["RS"]=np.array([a/b for a,b in zip(avg_gain,avg_loss)])
   df["RSI"]=100-(100/(1+df["RS"]))
   df.drop(["delta","gain","loss","RS"],axis=1, inplace=True)

   
def add_OBV(DF):
   df=DF.copy()
   df["daily_ret"]=df["Adj Close"].pct_change()
   df["direction"]=np.where(df["daily_ret"]>=0,1,-1)
   df["direction"][0]=0
   df["vol_adj"]=df["Volume"]*df["direction"]
   DF["OBV"]=df["vol_adj"].cumsum()
   
def add_ADX(DF,n):
   "function to calculate ADX"
   df2 = DF.copy()
   df2['H-L']=abs(df2['High']-df2['Low'])
   df2['H-PC']=abs(df2['High']-df2['Adj Close'].shift(1))
   df2['L-PC']=abs(df2['Low']-df2['Adj Close'].shift(1))
   df2['TR']=df2[['H-L','H-PC','L-PC']].max(axis=1,skipna=False)
   
   df2['DMplus']=np.where((df2['High']-df2['High'].shift(1))>(df2['Low'].shift(1)-df2['Low']),df2['High']-df2['High'].shift(1),0)
   df2['DMplus']=np.where(df2['DMplus']<0,0,df2['DMplus'])
   df2['DMminus']=np.where((df2['Low'].shift(1)-df2['Low'])>(df2['High']-df2['High'].shift(1)),df2['Low'].shift(1)-df2['Low'],0)
   df2['DMminus']=np.where(df2['DMminus']<0,0,df2['DMminus'])
   TRn = []
   DMplusN = []
   DMminusN = []
   TR = df2['TR'].tolist()
   DMplus = df2['DMplus'].tolist()
   DMminus = df2['DMminus'].tolist()
   for i in range(len(df2)):
      if i < n:
         TRn.append(np.NaN)
         DMplusN.append(np.NaN)
         DMminusN.append(np.NaN)
      elif i == n:
         TRn.append(df2['TR'].rolling(n).sum().tolist()[n])
         DMplusN.append(df2['DMplus'].rolling(n).sum().tolist()[n])
         DMminusN.append(df2['DMminus'].rolling(n).sum().tolist()[n])
      elif i > n:
         TRn.append(TRn[i-1] - (TRn[i-1]/n) + TR[i])
         DMplusN.append(DMplusN[i-1] - (DMplusN[i-1]/n) + DMplus[i])
         DMminusN.append(DMminusN[i-1] - (DMminusN[i-1]/n) + DMminus[i])
   df2['TRn'] = np.array(TRn)
   df2['DMplusN'] = np.array(DMplusN)
   df2['DMminusN'] = np.array(DMminusN)
   df2['DIplusN']=100*(df2['DMplusN']/df2['TRn'])
   df2['DIminusN']=100*(df2['DMminusN']/df2['TRn'])
   df2['DIdiff']=abs(df2['DIplusN']-df2['DIminusN'])
   df2['DIsum']=df2['DIplusN']+df2['DIminusN']
   df2['DX']=100*(df2['DIdiff']/df2['DIsum'])
   ADX = []
   DX = df2['DX'].tolist()
   for j in range(len(df2)):
      if j < 2*n-1:
         ADX.append(np.NaN)
      elif j == 2*n-1:
         ADX.append(df2['DX'][j-n+1:j+1].mean())
      elif j > 2*n-1:
         ADX.append(((n-1)*ADX[j-1] + DX[j])/n)
   del df2
   DF['ADX']=np.array(ADX)




    
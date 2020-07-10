import statsmodels.api as sm
import numpy as np

def add_slope(data,n):
    ser=data["Adj Close"]
    slopes=[i*0 for i in range(n-1)]
    for i in range(n,len(ser)+1):
        y=ser[i-n:i]
        x=np.array(range(n))
        y_scaled=(y-y.min())/(y.max()-y.min())
        x_scaled=(x-x.min())/(x.max() - x.min())
        x_scaled=sm.add_constant(x_scaled)
        model=sm.OLS(y_scaled,x_scaled)
        results=model.fit()
        slopes.append(results.params[-1])

    slope_angle=(np.rad2deg(np.arctan(np.array(slopes))))
    data["slope"]=np.array(slope_angle)

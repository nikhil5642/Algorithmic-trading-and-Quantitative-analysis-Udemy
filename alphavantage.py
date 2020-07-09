from alpha_vantage.timeseries import TimeSeries
ALPHA_VANTAGE_API_KEY = 'F80HDDVZM50CKH5C'
ts = TimeSeries(key=ALPHA_VANTAGE_API_KEY, output_format='pandas')
intraday_data, data_info = ts.get_intraday('aapl', outputsize='full', interval='1min')
import pandas_datareader.data as web
import os
import datetime
import yfinance as yf
import quandl


ibm = 'IBM'
aapl = 'AAPL'  # or 'AAPL.US'
sp500 = '^GSPC'
start = datetime.datetime(1901, 1, 1)
end = datetime.datetime(2001, 12, 15)


# using Alpha Vantage API
""" os.environ["ALPHAVANTAGE_API_KEY"] = "1XM7Y6VSQ7BIWFMD"
# IBM
df_av_ibm = web.DataReader(aapl, "av-daily", start=start, end=end, api_key="os.getenv('ALPHAVANTAGE_API_KEY')")
df_av_ibm.info()
print(df_av_ibm.head())

# AAPL
df_av_aapl = web.DataReader(aapl, "av-daily", start=start, end=end, api_key="os.getenv('ALPHAVANTAGE_API_KEY')")
df_av_aapl.info()
print(df_av_aapl.head())
 """
# using yahoo finance API
# using Ticker call
# yf_aapl = yf.Ticker(aapl)
# df_yf_aapl = yf_aapl.history(period="max")
# using download call
# # S&P500
# df_yf_sp500 = yf.download(sp500, start=start, end=end)
# print(df_yf_sp500.head())
# IBM
df_yf_ibm = yf.download(ibm, start=start, end=end)
print(df_yf_ibm.head())
# # AAPL
# df_yf_aapl = yf.download(aapl, start=start, end=end)
# print(df_yf_aapl.head())

# using quandl
""" quandl.ApiConfig.api_key = "uVFbTVxaHNb9y1ezJzbo"
tsk = "EOD"
df_ql = quandl.get(tsk+"/"+aapl, start_date=start, end_date=end)
df_ql.info()
print(df_ql.head()) """
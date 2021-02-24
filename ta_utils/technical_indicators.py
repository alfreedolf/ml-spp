######################################################################
# This file contains utility functions to conduct technical analysis #
# on a stock price.                                                  #
######################################################################
import numpy as np
# moving average
def moving_average(stock_price, window_size=20):
    return stock_price.rolling(window=window_size).mean()

# standard deviation
def std_dev(stock_price, window_size=20):
    return stock_price.rolling(window=window_size).std()

# stock price volatility
def volatility(stock_price, window_size=20):
    sv = std_dev(stock_price, window_size=window_size)
    vol = sum(np.square(sv.values[window_size-1:]))/len(sv.values)
    return vol

# bollinger bands
def bollinger_bands(stock_price, window_size=20, num_of_std=2):

    rolling_mean = moving_average(stock_price, window_size=window_size)
    rolling_std  = std_dev(stock_price, window_size=window_size)
    upper_band = rolling_mean + (rolling_std*num_of_std)
    lower_band = rolling_mean - (rolling_std*num_of_std)

    return rolling_mean, upper_band, lower_band



    
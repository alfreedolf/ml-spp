######################################################################
# This file contains utility functions to conduct technical analysis #
# on a stock price.                                                  #
######################################################################
import numpy as np
import pandas as pd


# moving average
def moving_average(time_series, window_size=20, fwd_fill_to_end=0):
    """
    A Simple Moving Average (SMA) function
    :param time_series: a pandas time series input containing numerical values
    :param window_size: a window size used to compute the SMA
    :param fwd_fill_to_end: index from which computation must stop and propagate last value
    :return: Simple Moving Average time series
    """
    if fwd_fill_to_end <= 0:
        return time_series.rolling(window=window_size).mean()
    else:
        sma = time_series.rolling(window=window_size).mean()
        sma[-fwd_fill_to_end:] = sma.iloc[-fwd_fill_to_end]
        return sma


# standard deviation
def std_dev(stock_price_time_series, window_size=20, fwd_fill_to_end=0):
    return stock_price_time_series.rolling(window=window_size).std()


# stock price volatility
def volatility(stock_price_time_series, window_size=20, fwd_fill_to_end=0):
    sv = std_dev(stock_price_time_series, window_size=window_size)
    vol = sum(np.square(sv.values[window_size - 1:])) / len(sv.values)
    return vol


# bollinger bands
def bollinger_bands(stock_price_time_series, window_size=20, num_of_std=2, fwd_fill_to_end=0):
    rolling_mean = moving_average(stock_price_time_series, window_size=window_size)
    rolling_std = std_dev(stock_price_time_series, window_size=window_size)
    upper_band = rolling_mean + (rolling_std * num_of_std)
    lower_band = rolling_mean - (rolling_std * num_of_std)

    return rolling_mean, upper_band, lower_band

# momentum

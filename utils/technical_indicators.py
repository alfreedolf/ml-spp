######################################################################
# This file contains utility functions to conduct technical analysis #
# on a stock price.                                                  #
######################################################################
import numpy as np
import pandas as pd


# moving average
def moving_average(time_series, window_size=20, fwd_fill_to_end=0):
    """
    Computes a Simple Moving Average (SMA) function on a time series
    :param time_series: a pandas time series input containing numerical values
    :param window_size: a window size used to compute the SMA
    :param fwd_fill_to_end: index from which computation must stop and propagate last value
    :return: Simple Moving Average time series
    """
    if fwd_fill_to_end <= 0:
        sma = time_series.rolling(window=window_size).mean()
    else:
        sma = time_series.rolling(window=window_size).mean()
        sma[-fwd_fill_to_end:] = sma.iloc[-fwd_fill_to_end]

    '''
    Moving average feature is empty for the first *n* days, where *n* is the window size,
    so I'll use some backfill to fill NaN values
    '''
    sma.fillna(method='backfill', inplace=True)
    return sma


# standard deviation
def std_dev(time_series, window_size=20, fwd_fill_to_end=0):
    """
    Computes Standard Deviation (STD) function on a time series
    :param time_series: a pandas input time series containing numerical values
    :param window_size: a window size used to compute the STD
    :param fwd_fill_to_end: index from which computation must stop and propagate last value
    :return: Standard Deviation time series
    """
    if fwd_fill_to_end <= 0:
        std = time_series.rolling(window=window_size).std()
    else:
        std = time_series.rolling(window=window_size).std()
        std[-fwd_fill_to_end:] = std.iloc[-fwd_fill_to_end]
    return std


# stock price volatility
def volatility(time_series, window_size=20):
    """
    Computes volatility on a time series
    :param time_series: a pandas input time series containing numerical values
    :param window_size: a window size used to compute the volatility value
    :return: volatility of the time series values
    """
    sv = std_dev(time_series, window_size=window_size)
    vol = sum(np.square(sv.values[window_size - 1:])) / len(sv.values)
    return vol


# Bollinger bands
def bollinger_bands(stock_price_time_series, window_size=20, num_of_std=2, fwd_fill_to_end=0):
    """
    Computes Bollinger bands function values on a time series
    :param stock_price_time_series: stock prices time series on which bollinger bands are computed
    :param window_size: window size used for moving average and standard deviation computation
    :param num_of_std: number of standard deviations used for
    :param fwd_fill_to_end: index from which computation must stop and propagate last value
    :return: moving average time series, bollinger upper band, bollinger lower band
    """
    rolling_mean = moving_average(stock_price_time_series, window_size=window_size, fwd_fill_to_end=fwd_fill_to_end)
    rolling_std = std_dev(stock_price_time_series, window_size=window_size, fwd_fill_to_end=fwd_fill_to_end)
    upper_band = rolling_mean + (rolling_std * num_of_std)
    lower_band = rolling_mean - (rolling_std * num_of_std)

    return rolling_mean, upper_band, lower_band

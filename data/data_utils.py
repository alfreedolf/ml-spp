# This file contains data utility to slice input data.
# The slicing has been optimized to comply to DeepAR algorithm best practices
# as in https://docs.aws.amazon.com/sagemaker/latest/dg/deepar.html

import datetime


def train_test_valid_split(ts, prediction_length):
    """
    This function slices input Time Series ts into train, test and validation set with the following ratio:
    * Training set will start at the beginning of the input time series and is truncated right before
        2*prediction_length elements from the end.
    * Test set will start from the beginning of the time series and stops at exactly prediction_length elements
        from the end of the input time series. Hence, it will include the training set and it will add exactly
        prediction_length more to it.
    * Validation set will be the last prediction_length elements from the input time series.

    :param ts: Time series to be predicted
    :param prediction_length: prediction length to be used for data splitting
    :return: train set, test set and validation set
    """
    train_size = int(len(ts) - prediction_length * 2)
    test_size = int(len(ts) - prediction_length)
    valid_size = prediction_length
    ts_train, ts_test, ts_valid = ts[0:train_size].copy(), ts[0:test_size].copy(), ts[test_size:].copy()
    return ts_train, ts_test, ts_valid

# TODO
def weekend_removal(ts):
    """
    This function removes Week End days from time series index
    :param ts: input time series with daily frequency
    :return: a time series where all the days are week days
    """
    already_used_days = []
    for i, d in enumerate(ts):
        week_day_num = d.index.day().weekday()

        if week_day_num > 5:
            delta = datetime.timedelta((8 - week_day_num))
            ts.index[i] = d.index + delta
            already_used_days.append(d.index[i])
        else:
            ts.index[i], already_used_days = adjust_week_day(ts.index[i], already_used_days)

    return ts

# TODO
def adjust_week_day(current_day, already_used_days):
    week_day_num = current_day.index.day().weekday()
    if current_day in already_used_days:
        adjust_week_day(current_day.day + datetime.timedelta((8 - week_day_num)))
    return None, None
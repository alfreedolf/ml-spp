# This file contains data utility to slice input data

def train_test_valid_split(ts, prediction_length):
    """

    This function slices input Time Series ts into train, test and validation set with the following ratio:
    * Training set will start at the beginning of the input time series and is truncated right before
    3*prediction_length elements from the end.
    * Test set will start from the 3*prediction_length from the end and stops leaving exactly prediction_length elements
    to the end of the input time series. Hence, it will be exactly 2*prediction_length elements long.
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

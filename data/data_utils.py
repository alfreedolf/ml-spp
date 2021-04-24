# This file contains data utility to slice input data.
# The slicing has been optimized to comply to DeepAR algorithm best practices
# as in https://docs.aws.amazon.com/sagemaker/latest/dg/deepar.html

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

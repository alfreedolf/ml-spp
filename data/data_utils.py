# * new function
def train_test_valid_split(ts, prediction_length):
    train_size = int(len(ts)-prediction_length*2)
    test_size = int(len(ts)-prediction_length)
    valid_size = prediction_length
    ts_train, ts_test, ts_valid = ts[0:train_size].copy(),\
                                                ts[0:test_size].copy(),\
                                                ts[test_size:].copy()
    return ts_train, ts_test, ts_valid
    
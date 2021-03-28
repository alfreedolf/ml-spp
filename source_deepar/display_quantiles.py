import matplotlib.pyplot as plt


def display_quantiles(prediction, target_ts=None, bench_mark_prediction=None, bench_mark_prediction_name=None):
    """
    Show predictions for input time series against comparison values
    """
    plt.figure(figsize=(12, 6))
    # get the target month of data
    if target_ts is not None:
        # target = target_ts[:]
        # plt.plot(range(len(target)), target, label='target')
        target_ts.plot()
    # get the quantile values at 10 and 90%
    p10 = prediction['0.1']
    p90 = prediction['0.9']
    # fill the 80% confidence interval
    plt.fill_between(p10.index, p10, p90, color='y', alpha=0.5, label='80% confidence interval')
    # plot the median prediction line
    prediction['0.5'].plot(label='prediction median')
    if bench_mark_prediction is not None:
        bench_mark_prediction.plot(label=bench_mark_prediction_name, color='r')
    plt.legend()
    plt.show()

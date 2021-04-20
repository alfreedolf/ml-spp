import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import numpy as np
import base64
from io import BytesIO
from datetime import datetime, timedelta


def display_quantiles(prediction, target_ts=None, benchmark_prediction=None, benchmark_prediction_name=None):
    """
    Show predictions for input time series against comparison values
    :param prediction:
    :param target_ts:
    :param benchmark_prediction:
    :param benchmark_prediction_name:
    """
    plt.figure(figsize=(12, 6))
    # get the target month of data
    if target_ts is not None:
        target_ts.plot()
    # get the quantile values at 10 and 90%
    p10 = prediction['0.1']
    p90 = prediction['0.9']
    # fill the 80% confidence interval
    plt.fill_between(p10.index, p10, p90, color='y', alpha=0.5, label='80% confidence interval')
    # plot the median prediction line
    prediction['0.5'].plot(label='prediction median')
    if benchmark_prediction is not None:
        benchmark_prediction.plot(label=benchmark_prediction_name, color='r')
    plt.legend()
    plt.show()


def display_quantiles_flask(prediction, target_ts=None, bench_mark_prediction=None,
                            bench_mark_prediction_name=None, start=None):
    """
    Show predictions for input time series against comparison values in a Flask application
    :param prediction:
    :param target_ts:
    :param bench_mark_prediction:
    :param bench_mark_prediction_name:
    :param start:
    :return: a <img> HTML5 element containing the plot
    """

    fig = Figure()
    ax = fig.subplots()
    if start is not None:
        # retrieving x-ticks
        if isinstance(start, str):
            start_date = datetime.strptime(start, "%Y-%m-%d %H:%M:%S").date()
        elif isinstance(start, datetime.datetime):
            start_date = start.date()
        elif isinstance(start, datetime.date):
            starte_date = start
        else:
            print("Enter only string or date as start values")
        x_ticks = [start_date + x * timedelta(days=1) for x in range(len(prediction['0.5']))]
        ax.set_xticklabels(["{}/{}".format(x_tick.day, x_tick.month) for x_tick in x_ticks])
    if target_ts is not None:
        ax.plot(target_ts, label='real Adjusted Close')

    # get the quantile values at 10 and 90%
    p10 = np.array(prediction['0.1'], dtype=float)
    p50 = np.array(prediction['0.5'], dtype=float)
    p90 = np.array(prediction['0.9'], dtype=float)

    # fill the 80% confidence interval
    ax.fill_between(range(0, len(p10)), p10, p90, color='y', alpha=0.5, label='80% confidence interval')

    # plot the median prediction line
    ax.plot(p50, label='prediction median')

    # plot benchmark data
    if bench_mark_prediction is not None:
        ax.plot(bench_mark_prediction, label=bench_mark_prediction_name, color='r')

    # adding legend
    ax.legend()

    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")

    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    data_str = f"<img src='data:image/png;base64,{data}'/>"
    return data_str

from datetime import date
import datetime
from flask import Flask, request, render_template
from numpy.lib.function_base import quantile
from source_deepar.display_quantiles import display_quantiles_flask
import json
import boto3

app = Flask(__name__)


@app.route("/")
def home():
    return render_template(
        "base.html"
    )


@app.route('/predict', methods=['POST'])
def predict():
    # retrieving data to be used as ground truth
    ticker_name = request.form['ticker_name']
    # dataset target of the prediction
    tgt_dataset = request.form['dataset']
    gt_dict = get_stock_data_from_s3_bucket(ticker_name, tgt_dataset)
    # retrieving ts start date
    # in_data_start = datetime.datetime.strptime(gt_dict['start'], "%Y-%m-%d %H:%M:%S")
    # start_date = in_data_start  + datetime.timedelta(days=len(gt_dict['target']))
    start_date = gt_dict['start']
    # retrieving target ts data
    target_ts = gt_dict['target']
    # retrieving benchmark data
    bk_dict = get_stock_data_from_s3_bucket(ticker_name, 'benchmark_test')
    benchmark_ts = bk_dict['target']

    # retrieving predicted data to be plot togheter with above data
    js_pred_data = request.form['predicted_data']
    pred_dict = json.loads(js_pred_data)['predictions']
    quantiles_dict = pred_dict[0]['quantiles']

    # displaying quantiles graph
    qp = display_quantiles_flask(quantiles_dict, target_ts=target_ts, bench_mark_prediction=benchmark_ts,
                                 bench_mark_prediction_name='SMA', start=start_date)
    return qp


@app.route('/predict_future', methods=['POST'])
def predict_future():
    # retrieving start date
    start_date = request.form['start_date']

    # retrieving predicted data to be plot togheter with above data
    js_pred_data = request.form['predicted_data']
    pred_dict = json.loads(js_pred_data)['predictions']
    quantiles_dict = pred_dict[0]['quantiles']

    # displaying quantiles graph
    qp = display_quantiles_flask(quantiles_dict, start=start_date + " {}:{}:{}".format("00", "00", "00"))
    return qp


def get_stock_data_from_s3_bucket(ticker_name, dataset):
    # S3 resource invocation
    s3_resource = boto3.resource('s3')
    # S3 bucket selection
    data_bucket_name = "stock-prediction-data-4327a669-7f13-48c7-aa4a-49a80b9e1e32"
    from source_deepar.lambda_stock_prediction import get_stock_data
    return get_stock_data(ticker_name=ticker_name,
                          s3_resource=s3_resource, s3_bucket=data_bucket_name, prefix=dataset)


if __name__ == '__main__':
    app.run(debug=True)

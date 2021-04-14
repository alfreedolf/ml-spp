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


@app.route('/predictfromdata', methods = ['POST'])
def predict_from_data():
    
    # retrieving data to be used as ground truth
    gt_dict = get_ground_truth_fromS3(request.form['ticker_name'])
    start_date = gt_dict['start']

    # retrieving data to be used for prediction
    js_pred_data = request.form['predicted_data']
    
    pred_dict = json.loads(js_pred_data)['predictions']
    quantiles_dict = pred_dict[0]['quantiles']

    

    # displaying quantiles graph
    qp = display_quantiles_flask(quantiles_dict, target_ts=gt_dict['target'],
            start=start_date)
    return qp

def get_ground_truth_fromS3(ticker_name):
    # S3 resource invocation
    s3_resource = boto3.resource('s3')
    # S3 bucket selection
    data_bucket_name = "stock-prediction-data-4327a669-7f13-48c7-aa4a-49a80b9e1e32"
    from source_deepar.deepar_lambda_function import get_json_stock_data
    return get_json_stock_data(ticker_name=ticker_name,\
        s3_resource=s3_resource, s3_bucket=data_bucket_name)
    

@app.route('/getmethod/<jsdata>')
def get_javascript_data(jsdata):
    return json.loads(jsdata)[0]
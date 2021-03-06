r"""
Stock prediction by means of DeepAR model, from a future date
"""
# We need to use the low-level library to interact with SageMaker since the SageMaker API
# is not available natively through Lambda.
import boto3
# we need to use json in order to interact with endpoint I/O
import json
import os


def lambda_handler(event, context):
    """
    This function handles POST request from REST AWS API Gateway,
    directed to SageMaker ML Model Prediction Endpoint.
    It will be the entry point of the entire module.
    :param event: externally generated event to be used to feed the SageMaker ML model endpoint.
    :param context: the context where the event has been triggered
    :return: a json formatted response from SageMaker ML model endpoint.
    """

    # S3 resource invocation
    s3_resource = boto3.resource('s3')
    # S3 bucket selection
    data_bucket_name = "put_here_data_bucket_name"
    # The SageMaker runtime is what allows us to invoke the endpoint that we've created.
    runtime = boto3.Session().client('sagemaker-runtime')

    request_body_dict = json.loads(event['body'])

    # Now we use the SageMaker runtime to invoke our endpoint, sending both ticker and start date if given
    if request_body_dict['start_date'] != "":
        response = runtime.invoke_endpoint(EndpointName='DeepAR-ml-spp',  # The name of the endpoint we created
                                           ContentType='application/json',  # The data format that is expected
                                           Body=encode_future_request(request_body=request_body_dict,
                                                                      s3_resource=s3_resource,
                                                                      s3_bucket=data_bucket_name, prefix='valid'))
    # or only ticker name if no start date has been provided
    elif request_body_dict['ticker_name'] != "":
        response = runtime.invoke_endpoint(EndpointName='DeepAR-ml-spp',  # The name of the endpoint we created
                                           ContentType='application/json',  # The data format that is expected
                                           Body=encode_request(ticker_name=request_body_dict['ticker_name'],
                                                               s3_resource=s3_resource, s3_bucket=data_bucket_name,
                                                               prefix='train'))

    # The response is an HTTP response whose body contains the result of our inference
    result = response['Body'].read().decode('utf-8')

    # print data for debug purposes
    print(result)

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
        'body': str(result)
    }


def encode_future_request(request_body, s3_resource, s3_bucket, prefix) -> bytes:
    """
    Encodes a request to be fed to the SageMaker endpoint from a start date on.
    :param request_body: a dictionary that describe what kind of prediction is desired
    :param s3_resource: AWS S3 resource identifier
    :param s3_bucket: AWS S3 bucket name
    :param prefix: AWS S3 bucket inner path
    :return: a json object containing a request ready to be sent to the endpoint
    """

    start_date = request_body['start_date']
    ticker_name = request_body['ticker_name']
    target_data = get_stock_data(ticker_name=ticker_name, s3_resource=s3_resource, s3_bucket=s3_bucket, prefix=prefix)[
        'target']
    instance = [{"start": start_date, "target": target_data}]

    configuration = {
        "num_samples": 100,
        "output_types": ["quantiles"],
        "quantiles": ["0.1", "0.5", "0.9"],
    }
    http_request_data = {"instances": instance, "configuration": configuration}
    return json.dumps(http_request_data).encode("utf-8")


def encode_request(ticker_name, s3_resource, s3_bucket, prefix) -> bytes:
    """
    Encodes a request to be fed to the SageMaker endpoint
    :param s3_bucket: S3 bucket where to find json data
    :param s3_resource: s3 resource where the data is located
    :param ticker_name: a string indicating which stock has to be predicted.
                        Possible values: 'IBM', 'AAPL', 'AMZN', 'GOOGL'.
    :param prefix: data source to be used for prediction (test, validation, etc.)
    :return: a json string containing a request ready to be sent to the endpoint
    """
    instances = [get_stock_data(ticker_name, s3_resource=s3_resource,
                                s3_bucket=s3_bucket, prefix=prefix)]
    configuration = {
        "num_samples": 100,
        "output_types": ["quantiles"],
        "quantiles": ["0.1", "0.5", "0.9"],
    }
    http_request_data = {"instances": instances, "configuration": configuration}
    return json.dumps(http_request_data).encode("utf-8")


def get_ibm_adj_cls_from_s3(s3_resource, bucket_name, prefix='') -> dict:
    """
    Load IBM stock json serialized data from S3 resource
    :param prefix: prefix of the path where the file is located
    :param s3_resource: s3 resource to get data from
    :param bucket_name: s3 bucket to get data from
    :return: dict object containing IBM stock price adjusted close from S3 archived JSON
    """
    ibm_filename = "IBM.json"
    complete_path = os.path.join(prefix, ibm_filename)
    json_object = s3_resource.Object(bucket_name, complete_path)
    file_content = json_object.get()['Body'].read().decode('utf-8')
    json_content = json.loads(file_content)
    return json_content


def get_amazon_adj_cls_from_s3(s3_resource, bucket_name, prefix='') -> dict:
    """
    Load IBM stock json serialized data from S3 resource
    :param prefix: prefix of the path where the find will be placed
    :param s3_resource: s3 resource to get data from
    :param bucket_name: s3 bucket to get data from
    :return: dict object containing AMZN stock price adjusted close from S3 archived JSON
    """
    amzn_filename = "AMZN.json"
    complete_path = os.path.join(prefix, amzn_filename)
    json_object = s3_resource.Object(bucket_name, complete_path)
    file_content = json_object.get()['Body'].read().decode('utf-8')
    json_content = json.loads(file_content)
    return json_content


def get_apple_adj_cls_from_s3(s3_resource, bucket_name, prefix='') -> dict:
    """
    Load Apple Inc. stock json serialized data from S3 resource
    :param prefix: prefix of the path where the file is located
    :param s3_resource: s3 resource to get data from
    :param bucket_name: s3 bucket to get data from
    :return: json object containing Apple Inc. stock price adjusted close
    """
    aapl_filename = "AAPL.json"
    complete_path = os.path.join(prefix, aapl_filename)
    json_object = s3_resource.Object(bucket_name, complete_path)
    file_content = json_object.get()['Body'].read().decode('utf-8')
    json_content = json.loads(file_content)
    return json_content


def get_google_adj_cls_from_s3(s3_resource, bucket_name, prefix='') -> dict:
    """
    Load Alphabet Inc. stock json serialized data from S3 resource
    :param prefix: prefix of the path where the file is located
    :param s3_resource: s3 resource to get data from
    :param bucket_name: s3 bucket to get data from
    :return: json object containing Alphabet Inc. stock price adjusted close
    """
    googl_filename = "GOOGL.json"
    complete_path = os.path.join(prefix, googl_filename)
    json_object = s3_resource.Object(bucket_name, complete_path)
    file_content = json_object.get()['Body'].read().decode('utf-8')
    json_content = json.loads(file_content)
    return json_content


def get_stock_data(ticker_name, s3_resource, s3_bucket, prefix='') -> dict:
    """
    Retrieves adjusted close data from S3
    :param s3_bucket: the S3 bucket containing the files to be
    :param s3_resource: the S3 resource to be used to access the file
    :param ticker_name: ticker name, one among IBM, AAPL, AMZN, GOOGL
    :param prefix: the folder where the file is located inside the S3 bucket
    :return: dictionary data about the ticker_name stock, retrieved from an S3 resident JSON file.
    """
    if ticker_name.upper() == "IBM":
        return get_ibm_adj_cls_from_s3(s3_resource, s3_bucket, prefix)
    elif ticker_name.upper() == "AMZN":
        return get_amazon_adj_cls_from_s3(s3_resource, s3_bucket, prefix)
    elif ticker_name.upper() == "AAPL":
        return get_apple_adj_cls_from_s3(s3_resource, s3_bucket, prefix)
    elif ticker_name.upper() == "GOOGL":
        return get_google_adj_cls_from_s3(s3_resource, s3_bucket, prefix)
    else:
        # TODO: add input error handling
        return None

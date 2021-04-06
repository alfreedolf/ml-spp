# We need to use the low-level library to interact with SageMaker since the SageMaker API
# is not available natively through Lambda.
import boto3
# we need to use json in order to interact with endpoint I/O
import json
import os


def lambda_handler(event, context):
    # sagemaker session retrieve:
    # TODO: check if it's feasible to retrieve SageMaker session from here
    sagemaker = boto3.client('sagemaker')
    sagemaker_session = sagemaker.Session()
    # S3 resource invocation
    resource = boto3.resource('s3')
    # S3 bucket selection

    bucket = "stock-prediction-data-4327a669-7f13-48c7-aa4a-49a80b9e1e32"

    # The SageMaker runtime is what allows us to invoke the endpoint that we've created.
    runtime = boto3.Session().client('sagemaker-runtime')

    # >> Something
    json_data = get_json_stock_data(event['ticker_name'], resource, bucket)
    # Now we use the SageMaker runtime to invoke our endpoint, sending the review we were given
    response = runtime.invoke_endpoint(EndpointName='DeepAR-ml-spp',  # The name of the endpoint we created
                                       ContentType='application/json',  # The data format that is expected
                                       Body=encode_request(json_data,
                                                           event['start_date']))  # The actual prediction requeste

    # The response is an HTTP response whose body contains the result of our inference
    result = response['Body'].read().decode('utf-8')

    # Round the result so that our web app only gets '1' or '0' as a response.
    result = round(float(result))

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'text/plain', 'Access-Control-Allow-Origin': '*'},
        'body': str(result)
    }


def encode_request(ticker_name, start_date, s3_path):
    """
    Encodes a request to be fed to the SageMaker endpoing
    :param s3_path: where to find json data on S3
    :param ticker_name: a string indicating which stock has to be predicted.
                        Possible values: 'IBM', 'AAPL', 'AMZN', 'GOOGL'.
    :param start_date: start date from which to predict from
    :return: a json object containing a request ready to be sent to the endpoint
    """
    instances = [get_json_stock_data(ticker_name, start_date, s3_path)]
    configuration = {
        "num_samples": 100,
        "output_types": ["quantiles"],
        "quantiles": ["0.1", "0.5", "0.9"],
    }
    http_request_data = {"instances": instances, "configuration": configuration}
    return json.dumps(http_request_data).encode("utf-8")


def get_ibm_json_from_s3(s3_resource, bucket_name, prefix=''):
    """
    Load IBM stock json data from S3 resource
    :param prefix: prefix of the path where the file is located
    :param s3_resource: s3 resource to get data from
    :param bucket_name: s3 bucket to get data from
    :return: json object containing IBM stock price adjusted close
    """
    ibm_filename = "IBM.json"
    complete_path = os.path.join(prefix, ibm_filename)
    json_object = s3_resource.Object(bucket_name, complete_path)
    file_content = json_object.get()['Body'].read().decode('utf-8')
    json_content = json.loads(file_content)
    return json_content


def get_amzn_json_from_s3(s3_resource, bucket_name, prefix=''):
    """
    Load AMZN stock json data from S3 resource
    :param prefix: prefix of the path where the find will be placed
    :param s3_resource: s3 resource to get data from
    :param bucket_name: s3 bucket to get data from
    :return: json object containing IBM stock price adjusted close
    """
    amzn_filename = "AMZN.json"
    complete_path = os.path.join(prefix, amzn_filename)
    json_object = s3_resource.Object(bucket_name, complete_path)
    file_content = json_object.get()['Body'].read().decode('utf-8')
    json_content = json.loads(file_content)
    return json_content


def get_aapl_json_from_s3(s3_resource, bucket_name, prefix=''):
    """
    Load AAPL stock json data from S3 resource
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


def get_googl_json_from_s3(s3_resource, bucket_name, prefix=''):
    """
    Load GOOGL stock json data from S3 resource
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


def get_json_stock_data(ticker_name, s3_resource, s3_bucket):
    """
    Retrieves json data from S3
    :param s3_bucket: the S3 bucket containing the files to be
    :param s3_resource: the S3 resource to be used to access the file
    :param ticker_name: ticker name, one among IBM, AAPL, AMZN, GOOGL
    :param s3_path: a string indicating where to find the json file on S3
    :return:
    """
    if ticker_name.upper() == "IBM":
        return get_ibm_json_from_s3(s3_resource, s3_bucket)
    elif ticker_name.upper() == "AMZN":
        return get_amzn_json_from_s3(s3_resource, s3_bucket)
    elif ticker_name.upper() == "AAPL":
        return get_aapl_json_from_s3(s3_resource, s3_bucket)
    elif ticker_name.upper() == "GOOGL":
        return get_googl_json_from_s3(s3_resource, s3_bucket)
    else:
        return None
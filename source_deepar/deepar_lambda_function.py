# We need to use the low-level library to interact with SageMaker since the SageMaker API
# is not available natively through Lambda.
import boto3
# we need to use json in order to interact with endpoint I/O
import json
import os


def lambda_handler(event, context):

    # S3 resource invocation
    s3_resource = boto3.resource('s3')
    # S3 bucket selection
    data_bucket_name = "stock-prediction-data-4327a669-7f13-48c7-aa4a-49a80b9e1e32"
    # The SageMaker runtime is what allows us to invoke the endpoint that we've created.
    runtime = boto3.Session().client('sagemaker-runtime')

    # Now we use the SageMaker runtime to invoke our endpoint, sending the review we were given
    response = runtime.invoke_endpoint(EndpointName='DeepAR-ml-spp',  # The name of the endpoint we created
                                       ContentType='application/json',  # The data format that is expected
                                       Body=encode_request(event['body'], s3_resource, data_bucket_name))

    # The response is an HTTP response whose body contains the result of our inference
    result = response['Body'].read().decode('utf-8')

    # print data for debug purposes
    print(result)

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
        'body': str(result)
    }


def encode_request(ticker_name, s3_resource, s3_bucket):
    """
    Encodes a request to be fed to the SageMaker endpoint
    :param s3_bucket: S3 bucket where to find json data
    :param s3_resource: s3 resource where the data is located
    :param ticker_name: a string indicating which stock has to be predicted.
                        Possible values: 'IBM', 'AAPL', 'AMZN', 'GOOGL'.
    :return: a json object containing a request ready to be sent to the endpoint
    """
    instances = [get_json_stock_data(ticker_name, s3_resource=s3_resource, s3_bucket=s3_bucket)]
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


def get_json_stock_data(ticker_name, s3_resource, s3_bucket, prefix=''):
    """
    Retrieves json data from S3
    :param s3_bucket: the S3 bucket containing the files to be
    :param s3_resource: the S3 resource to be used to access the file
    :param ticker_name: ticker name, one among IBM, AAPL, AMZN, GOOGL
    :param prefix: the folder where the file is located inside the S3 bucket
    :return:
    """
    if ticker_name.upper() == "IBM":
        return get_ibm_json_from_s3(s3_resource, s3_bucket, prefix)
    elif ticker_name.upper() == "AMZN":
        return get_amzn_json_from_s3(s3_resource, s3_bucket, prefix)
    elif ticker_name.upper() == "AAPL":
        return get_aapl_json_from_s3(s3_resource, s3_bucket, prefix)
    elif ticker_name.upper() == "GOOGL":
        return get_googl_json_from_s3(s3_resource, s3_bucket, prefix)
    else:
        return None
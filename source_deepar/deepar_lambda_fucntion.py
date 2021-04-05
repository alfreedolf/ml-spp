# We need to use the low-level library to interact with SageMaker since the SageMaker API
# is not available natively through Lambda.
import boto3
# we need to use json in order to interact with endpoint I/O
import json


def lambda_handler(event, context):
    # sagemaker session retrieve:
    # TODO: check if it's feasible to retrieve SageMaker session from here
    sagemaker = boto3.client('sagemaker')
    sagemaker_session = sagemaker.Session()
    # S3 resource invocation
    s3 = boto3.resource('s3')
    # S3 bucket selection
    # TODO check if it's possible to use default bucket here, if not, select the proper bucket
    bucket = sagemaker_session.default_bucket()

    # The SageMaker runtime is what allows us to invoke the endpoint that we've created.
    runtime = boto3.Session().client('sagemaker-runtime')

    # Now we use the SageMaker runtime to invoke our endpoint, sending the review we were given
    response = runtime.invoke_endpoint(EndpointName='***ENDPOINT NAME HERE***',  # The name of the endpoint we created
                                       ContentType='application/json',  # The data format that is expected
                                       Body=encode_request(event['ticker_name'],
                                                           event['start_date']))  # The actual review

    # The response is an HTTP response whose body contains the result of our inference
    result = response['Body'].read().decode('utf-8')

    # Round the result so that our web app only gets '1' or '0' as a response.
    result = round(float(result))

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'text/plain', 'Access-Control-Allow-Origin': '*'},
        'body': str(result)
    }


def encode_request(ticker_name, start_date):
    """
    Encodes a request to be fed to the SageMaker endpoing
    :param ticker_name: a string indicating which stock has to be predicted.
                        Possible values: 'IBM', 'AAPL', 'AMZN', 'GOOGL'.
    :param start_date: start date from which to predict from
    :return: a json object containing a request ready to be sent to the endpoin
    """
    instances = [ticker_name2_json_obj(ticker_name, start=start_date)]
    configuration = {
        "num_samples": 100,
        "output_types": ["quantiles"],
        "quantiles": ["0.1", "0.5", "0.9"],
    }
    http_request_data = {"instances": instances, "configuration": configuration}
    return json.dumps(http_request_data).encode("utf-8")


def ticker_name2_json_obj(ticker_name, start):
    """
    Returns a json object containing the data relative to ticker_name and start date
    :param ticker_name:
    :param start:
    :return: json object containing data from
    """
    # get start time and target from the time series, ts
    if start is not None:
        start_index = start
        ts = ts.loc[start_index:]

        if not dyn_feat:

            json_obj = {"start": str(pd.to_datetime(start_index)),
                        "target": list(ts.loc[:, target_column])}
        else:
            # populating dynamic features array
            df_dyn_feat = ts.loc[:, dyn_feat]
            dyn_feat_list = []
            for feat in df_dyn_feat:
                dyn_feat_list.append(list(df_dyn_feat[feat]))

            # creating json object
            json_obj = {"start": str(pd.to_datetime(start_index)),
                        "target": list(ts.loc[:, target_column]),
                        "dynamic_feat": list(dyn_feat_list)}

    else:
        if not dyn_feat:
            json_obj = {"start": str(ts.index[0]),
                        "target": list(ts.loc[:, target_column])}

        else:
            # populating dynamic features array
            df_dyn_feat = ts.loc[:, dyn_feat]
            dyn_feat_list = []
            for feat in df_dyn_feat:
                dyn_feat_list.append(list(df_dyn_feat[feat]))

            # creating json object
            json_obj = {"start": str(ts.index[0]), "target": list(ts.loc[:, target_column]),
                        "dynamic_feat": list(dyn_feat_list)}

    return json_obj

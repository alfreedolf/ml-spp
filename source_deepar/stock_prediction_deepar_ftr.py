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

    runtime = boto3.Session().client('sagemaker-runtime')

    # Now we use the SageMaker runtime to invoke our endpoint, sending the review we were given
    response = runtime.invoke_endpoint(EndpointName='DeepAR-ml-spp',  # The name of the endpoint we created
                                       ContentType='application/json',  # The data format that is expected
                                       Body=encode_request(event['body']))

    # The response is an HTTP response whose body contains the result of our inference
    result = response['Body'].read().decode('utf-8')

    # print data for debug purposes
    print(result)

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
        'body': str(result)
    }


def encode_request(start_date):
    """
    Encodes a request to be fed to the SageMaker endpoint from a start date on
    :return: a json object containing a request ready to be sent to the endpoint
    """
    instance = [{"start": start_date, "target": []}]

    configuration = {
        "num_samples": 100,
        "output_types": ["quantiles"],
        "quantiles": ["0.1", "0.5", "0.9"],
    }
    http_request_data = {"instances": instance, "configuration": configuration}
    return json.dumps(http_request_data).encode("utf-8")



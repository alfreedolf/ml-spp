import json
import boto3

# from source_deepar.deepar_lambda_function import get_ibm_json_from_s3

import os
import uuid


def create_bucket_name(bucket_prefix):
    # The generated bucket name must be between 3 and 63 chars long
    return ''.join([bucket_prefix, str(uuid.uuid4())])


def create_bucket(bucket_prefix, s3_connection):
    session = boto3.session.Session()
    current_region = session.region_name
    bucket_name = create_bucket_name(bucket_prefix)
    bucket_response = s3_connection.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={
            'LocationConstraint': current_region})
    print(bucket_name, current_region)
    return bucket_name, bucket_response


s3_resource = boto3.resource('s3')

# data_bucket = create_bucket(bucket_prefix='stock-prediction-data-', s3_connection=s3_resource)
# data_bucket_name = data_bucket[0]

source_bucket = "sagemaker-eu-central-1-172877690028"
data_bucket_name = "stock-prediction-data-4327a669-7f13-48c7-aa4a-49a80b9e1e32"


def copy_to_bucket(src_bucket_name, src_prefix, dst_bucket_name, dst_prefix, file_name):
    """

    :param src_bucket_name:
    :param dst_bucket_name:
    :param src_prefix:
    :param dst_prefix:
    :param file_name:
    :return:
    """
    src_complete_file_name = os.path.join(src_prefix, file_name)

    copy_source = {
        'Bucket': src_bucket_name,
        'Key': src_complete_file_name
    }

    dst_complete_file_name = os.path.join(dst_prefix, file_name)
    s3_resource.Object(dst_bucket_name, dst_complete_file_name).copy(copy_source)


# test
copy_to_bucket(src_bucket_name=source_bucket, src_prefix='stock_deepar/json/test',
               dst_bucket_name=data_bucket_name,  dst_prefix='test', file_name='IBM.json')
copy_to_bucket(src_bucket_name=source_bucket, src_prefix='stock_deepar/json/test',
               dst_bucket_name=data_bucket_name, dst_prefix='test', file_name='AAPL.json')
copy_to_bucket(src_bucket_name=source_bucket, src_prefix='stock_deepar/json/test',
               dst_bucket_name=data_bucket_name, dst_prefix='test', file_name='AMZN.json')
copy_to_bucket(src_bucket_name=source_bucket, src_prefix='stock_deepar/json/test',
               dst_bucket_name=data_bucket_name, dst_prefix='test', file_name='GOOGL.json')

# benchmark
copy_to_bucket(src_bucket_name=source_bucket, src_prefix='stock_deepar/json/valid',
               dst_bucket_name=data_bucket_name, dst_prefix='valid', file_name='IBM.json')
copy_to_bucket(src_bucket_name=source_bucket, src_prefix='stock_deepar/json/valid',
               dst_bucket_name=data_bucket_name, dst_prefix='valid', file_name='AAPL.json')
copy_to_bucket(src_bucket_name=source_bucket, src_prefix='stock_deepar/json/valid',
               dst_bucket_name=data_bucket_name, dst_prefix='valid', file_name='AMZN.json')
copy_to_bucket(src_bucket_name=source_bucket, src_prefix='stock_deepar/json/valid',
               dst_bucket_name=data_bucket_name, dst_prefix='valid', file_name='GOOGL.json')

# benchmark
copy_to_bucket(src_bucket_name=source_bucket, src_prefix='stock_deepar/json/benchmark',
               dst_bucket_name=data_bucket_name, dst_prefix='benchmark', file_name='IBM.json')
copy_to_bucket(src_bucket_name=source_bucket, src_prefix='stock_deepar/json/benchmark',
               dst_bucket_name=data_bucket_name, dst_prefix='benchmark', file_name='AAPL.json')
copy_to_bucket(src_bucket_name=source_bucket, src_prefix='stock_deepar/json/benchmark',
               dst_bucket_name=data_bucket_name, dst_prefix='benchmark', file_name='AMZN.json')
copy_to_bucket(src_bucket_name=source_bucket, src_prefix='stock_deepar/json/benchmark',
               dst_bucket_name=data_bucket_name, dst_prefix='benchmark', file_name='GOOGL.json')

# sagemaker = boto3.client('sagemaker')
# sagemaker = boto3.Session().client('sagemaker')
# sagemaker_session = sagemaker
# S3 resource invocation

# S3 bucket selection
# bucket = sagemaker_session.default_bucket()

from source_deepar.deepar_lambda_function import get_stock_data

ibm_json = get_stock_data('IBM', s3_resource, data_bucket_name)
aapl_json = get_stock_data('AAPL', s3_resource, data_bucket_name)
amzn_json = get_stock_data('AMZN', s3_resource, data_bucket_name)
googl_json = get_stock_data('GOOGL', s3_resource, data_bucket_name)
print(ibm_json)
print(aapl_json)
print(amzn_json)
print(googl_json)

# from source_deepar.deepar_lambda_function import encode_request

# # feed data to endpoint
# endpoint_name = 'DeepAR-ml-spp'
# # The SageMaker runtime is what allows us to invoke the endpoint that we've created.
# runtime = boto3.Session().client('sagemaker-runtime')
# # Now we use the SageMaker runtime to invoke our endpoint, sending the review we were given
# response = runtime.invoke_endpoint(EndpointName='DeepAR-ml-spp',  # The name of the endpoint we created
#                                    ContentType='application/json',  # The data format that is expected
#                                    Body=encode_request("IBM", s3_resource, data_bucket_name))
# result = response['Body'].read().decode('utf-8')
# print(result)

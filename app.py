from chalice import Chalice
from chalice import BadRequestError
import json
import boto3
# import boto3, os, base64,ast
# import numpy as np


app = Chalice(app_name='SugarBeetClassifier')
app.debug = True

@app.route('/', methods=['POST'])
def index():
    body = app.current_request.json_body
    if 'url' not in body:
        raise BadRequestError('Missing url data')
    # if 'ENDPOINT_NAME' not in os.environ:
        # raise BadRequestError('Missing endpoint')

    input_url = json.dumps(body)
    endpoint = 'pytorch-inference-2020-09-14-08-59-57-063'
    # endpoint = os.environ['ENDPOINT_NAME']

    runtime = boto3.Session().client(service_name='sagemaker-runtime',region_name='eu-west-1')
    response = runtime.invoke_endpoint(EndpointName= endpoint,ContentType='application/json',Body=input_url)

    return {'response':response['Body'].read().decode()}
    # return input_url

# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#

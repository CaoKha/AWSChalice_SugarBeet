import boto3
import json
import numpy as np

# file_name = 'test/Agrostemma-githago_Cotyledon_Substrat3_12022020 (258).JPG'
endpoint_name = 'pytorch-inference-2020-09-14-08-59-57-063'
runtime = boto3.Session().client(service_name='runtime.sagemaker',region_name='eu-west-1')

# with open(file_name, 'rb') as f:
#         payload = f.read()
#         payload = bytearray(payload)

payload = json.dumps({"url":"https://www.dropbox.com/s/1t3enu6vjbxr1zr/Agrostemma-githago_Cotyledon_Substrat3_12022020%20%28258%29.JPG?raw=1"})

response = runtime.invoke_endpoint(EndpointName=endpoint_name, ContentType='application/json', Body=payload)
print(response['Body'].read().decode())
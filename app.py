from chalice import Chalice, Response
from chalice import BadRequestError
from chalicelib import db
import json, os, boto3, requests
from urllib.parse import parse_qs
import jinja2 
import re
import shutil


app = Chalice(app_name='SugarBeetClassifier')
app.debug = True

_DB = None
_ENDPOINT_NAME = 'pytorch-inference-2020-09-24-22-38-48-661'

def render(tpl_path, context):
    path, filename = os.path.split(tpl_path)
    return jinja2.Environment(loader=jinja2.FileSystemLoader(path or "./")).get_template(filename).render(context)

def get_app_db():
    global _DB
    if _DB is None:
        _DB = db.DynamoDBTodo(
            boto3.resource('dynamodb').Table(
                os.environ['APP_TABLE_NAME'])
        )
    return _DB


@app.route('/post', methods=['POST'], content_types=['application/x-www-form-urlencoded'])
def index():
    endpoint = _ENDPOINT_NAME
    
    parsed = parse_qs(app.current_request.raw_body.decode())
    url_image_list = parsed.get('url',[])
    url_image = url_image_list[0]
    # img_data = requests.get(url_image).content
    # with open('./chalicelib/sample.jpg','wb') as handler:
    #     handler.write(img_data)

    runtime = boto3.Session().client(service_name='sagemaker-runtime',region_name='eu-west-1')
    response = runtime.invoke_endpoint(EndpointName= endpoint,ContentType='application/json',Body=url_image)
    
    uid = get_app_db().add_item(description=response['Body'].read().decode())
    response_db = get_app_db().get_item(uid)
    data = json.loads(response_db.get('description'))
    tree_type = re.search(r'.+?(?=_)',data['class']).group()
    growth_stage = re.search(r'(?<=_)[\w+.-]+',data['class']).group()
    template = render('chalicelib/templates/results.html',{'plant_type': tree_type, 'growth_stage': growth_stage, 'confidence': data['confidence'], 'image_url': url_image} )
    return Response(template, status_code=200, headers={"Content-Type":"text/html", "Access-Control-Allow-Origin":"*"})
    # template = render('chalicelib/templates/results.html',{'result': OBJECTS['class']})
    # return Response(template, status_code=200, headers={"Content-Type":"text/html", "Access-Control-Allow-Origin":"*"})

# @app.route('/result/{uid}',methods=['GET'])
# def get_result(uid):
#     response = get_app_db().get_item(uid)
    # OBJECTS = eval(response['Body'].read().decode())
    

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

# import main Flask class and request object
import os
import sys
# from xml.etree.ElementTree import QName
import werkzeug
import flask

import logging
import boto3
from botocore.exceptions import ClientError

from flask_restplus import Api, Resource, fields, reqparse
from flask import Flask
from dotenv import load_dotenv
from pdf_main import pdf_main
from lib.utils import bcolors, get_file_info

#from flask_ngrok import run_with_ngrok
#from pyngrok import conf, ngrok

load_dotenv()
API_KEY = os.getenv("API_KEY")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

# create the Flask app
app = Flask(__name__)
#run_with_ngrok(app)
#conf.get_default().auth_token = "2End8bHg73QOy1gk2bpVTeSKa1C_5NzfibXoYK6e14Sn8pL7n"
#conf.get_default().config_path = "/Users/galogonzalvo/.ngrok2/ngrok.yml"
#conf.get_default().region = "us"
# ngrok.set_auth_token("2End8bHg73QOy1gk2bpVTeSKa1C_5NzfibXoYK6e14Sn8pL7n")
# http_tunnel = ngrok.connect(5001)
# print (http_tunnel)

# Swagger
werkzeug.cached_property = werkzeug.utils.cached_property
# authorizations = {
#     'apikey': {
#         'type': 'apiKey',
#         'in': 'header',
#         'name': 'x-api-key'
#     }
#}

api = Api(app, title='PDF table and image extraction',
          description='Extract all images and tables from an input PDF file. Additionally, convert all tables to editable format (.docx, .xlsx, .tex)',
          contact='galo.gonzalvo@gmail.com')

ns_pdf = api.namespace(
    'extractFromPDF', description='Extract all images and tables from an input PDF file. Additionally, convert all tables to editable format (.docx, .xlsx, .tex)')


@ns_pdf.route('/')
class extractFromPDF(Resource):
    post_parser = api.parser()
    # The below only results in the ability to upload a single file from the SwaggerUI.
    post_parser.add_argument(
        'input_file', type=werkzeug.datastructures.FileStorage, location='files', help="Attach your input file (PDF or jpg/png table)", required=True)
    post_parser.add_argument(
        'extension',
        choices=('docx', 'xlsx', 'tex'),
        help='Format of editable output tables', required=True
    )

    @ns_pdf.expect(post_parser)
    @ns_pdf.doc(body=post_parser, responses={200: 'OK', 400: 'Bad Request', 401: 'Unauthorized', 500: 'Internal Server Error'})
    def post(self):
        try:
            #x_api_key = request.headers.get("x-api-key")
            input_file = self.post_parser.parse_args().get('input_file')
            format_output = self.post_parser.parse_args().get('extension')
            request_security_pdf(input_file.filename, '')
            fname, outftype = get_file_info(input_file.filename, format_output)       
            pdf_main(input_file, format_output)
            outputFile = f'/tmp/test-api/{fname}{outftype}'
            url_zip = uploadFile_ObjectPresignedUrl(outputFile, 'figures_and_tables/')
            return url_zip, 200
        except SystemExit as e:
            status_code = int(str(e)[:3])
            msg = str(e)[6:]
            return msg, status_code

def request_security_pdf(INPUT_FILE: str, X_API_KEY: str):
    '''
    Request Security

    input:
        INPUT_FILE: filename attached in the request (str)
        X_API_KEY: API Key Body (str)
    '''
    if API_KEY != X_API_KEY:
        response_msg = '401 - Invalid Request - Unauthorized Request - API Key is not valid'
        print(response_msg)
        sys.exit(response_msg)
    if not INPUT_FILE.endswith('.pdf') and not INPUT_FILE.endswith('.jpg') and not INPUT_FILE.endswith('.png'):
        response_msg = f'400 - Invalid Request - Invalid Input File Format {INPUT_FILE} (not a PDF/jpg/png file)'
        print(response_msg)
        sys.exit(response_msg)
    print(f"{bcolors.OKGREEN}Security PASS - API KEY CORRECT{bcolors.ENDC}")


def s3_create_presigned_url(object_name, expiration=3600):
    """Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """

    # Generate a presigned URL for the S3 object
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': S3_BUCKET_NAME,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response



def s3_upload_file(s3: object, input_file: str, path: str):
    '''
    Write file in S3 Bucket

    input:
        s3: object S3
        input_file: file to upload name (str)
        path: path to upload file in S3 Bucket (string)
    '''
    result = s3.Bucket(S3_BUCKET_NAME).upload_file(
        input_file, path + input_file.split('/')[-1])
    if result == None:
        print(
            f"{bcolors.OKGREEN}DONE: File {input_file.split('/')[-1]} has been written in S3 Bucket!{bcolors.ENDC}")
    else:
        response_msg = f'400 - FAIL: File {input_file} has NOT been written in S3 Bucket!'
        print(
            f"{bcolors.FAIL}FAIL: File {input_file} has NOT been written in S3 Bucket!{bcolors.ENDC}")
        sys.exit(response_msg)

def uploadFile_ObjectPresignedUrl(out_file: str, path: str):
    '''
    Upload PDF file

    input:
        - outputKey: name pdf file (str)
    '''
    s3_resource = s3_connection_resource()
    s3_upload_file(s3_resource, out_file, path)
    url = s3_create_presigned_url(path + out_file.split('/')[-1])
    print(
        f"{bcolors.OKGREEN}Presigned URL created {out_file.split('/')[-1]}...{bcolors.ENDC}")
    return url


def s3_connection_resource():
    '''
    Accessing the S3 buckets using boto3 client

    output:
        s3: bucket S3 (str)
    '''
    s3_client = boto3.client('s3',
                             aws_access_key_id=AWS_ACCESS_KEY_ID,
                             aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    s3_resource = boto3.resource('s3',
                                 aws_access_key_id=AWS_ACCESS_KEY_ID,
                                 aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    return s3_resource


# ------------------------------------------------------------------------
# MAIN - HEALTH DOCKER SERVER
# ------------------------------------------------------------------------


@app.route('/', methods=['GET'])
def main():
    return 'OK', 200


if __name__ == '__main__':
    app.run()

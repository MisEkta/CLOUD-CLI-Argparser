import boto3
import logging
from botocore.exceptions import ClientError
from botocore.client import Config


class S3:
    def __init__(self, aws_endpoint_url='http://localhost:4566', aws_access_key_id='test', aws_secret_access_key='test'):
        config = Config(signature_version='s3v4')
        self.s3 = boto3.resource('s3',
                                 endpoint_url=aws_endpoint_url,
                                 aws_access_key_id=aws_access_key_id,
                                 aws_secret_access_key=aws_secret_access_key,
                                 config=config)

    def create_bucket(self,bucket_name):
        try:
            self.s3.create_bucket(Bucket=bucket_name)
            print(f"Created bucket {bucket_name}")
        except ClientError as e:
            logging.error(e)
            
    def upload_file(self,bucket_name, file_name, object_name):
        try:
            self.s3.Bucket(bucket_name).upload_file(file_name, object_name)
            print(f"Uploaded {file_name} to {bucket_name} as {object_name}")
        except ClientError as e:
            logging.error(e)

    def download_file(self,bucket_name, object_name, file_name):
        try:
            self.s3.Bucket(bucket_name).download_file(object_name, file_name)
            print(f"Downloaded {object_name} from {bucket_name} to {file_name}")
        except ClientError as e:
            logging.error(e)

    def describe_file(self,bucket_name, object_name):
        try:
            obj = self.s3.Object(bucket_name, object_name)
            print(f"File {object_name} in bucket {bucket_name} has size {obj.content_length} bytes and was last modified on {obj.last_modified}")
        except ClientError as e:
            logging.error(e)
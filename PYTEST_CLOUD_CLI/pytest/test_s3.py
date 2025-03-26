import boto3
import sys
import os
import pytest


# Add the CLOUD_CLI directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'CLOUD_CLI'))
from ec2 import EC2
from s3 import S3
from cli_argpar import aws_s3, aws_ec2

@pytest.fixture(scope="module")
def s3_client():
    return S3()

@pytest.fixture(scope="module")
def bucket_name():
    return "test-bucket"


#testing create function
def test_create(s3_client, bucket_name):
    s3_client.create_bucket(bucket_name)
    print("create done")
    assert True

#testing upload function
def test_upload(s3_client, bucket_name):
    file_name = "test.txt"
    object_name = "uploaded_text.txt"
    
    # Create a text file in real-time
    with open(file_name, "w") as file:
        file.write(input("Enter some text: "))
    
    s3_client.create_bucket(bucket_name)  # Ensure the bucket is created
    s3_client.upload_file(bucket_name, file_name, object_name)
    
    # Clean up the created file
    os.remove(file_name)
    
    assert True

#testing download function
def test_download(s3_client, bucket_name):
    s3_client.create_bucket(bucket_name)  # Ensure the bucket is created
    s3_client.download_file(bucket_name, "uploaded_text.txt", "downloaded_test.txt")
    print("download done")
    assert os.path.exists("downloaded_test.txt")
    os.remove("downloaded_test.txt")
    assert True


#testing describe function
def test_describe(s3_client, bucket_name):
    s3_client.create_bucket(bucket_name)  # Ensure the bucket is created
    s3_client.describe_file(bucket_name, "uploaded_text.txt")
    print("describe done")
    assert True
import boto3
# s3=S3()
# ec2=EC2()
# print("done")
import sys
import os

# Add the CLOUD_CLI directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'CLOUD_CLI'))

import pytest
from ec2 import EC2
from s3 import S3
from cli_argpar import aws_s3, aws_ec2

# s3 = S3()
# ec2 = EC2()
# s3.create_bucket("test-bucket")
# print("bucket created")
instance_id=" "
#testing  create instance

def test_create_instance():
    ec2=EC2()
    instance_id=ec2.create_instance("ami-123456", "t2.micro", "test-key")
    assert True
    
#testing start instance
def test_start_instance():
    ec2=EC2()
    ec2.start_instance(instance_id)
    assert True

#testing stop instance
def test_stop_instance():
    ec2=EC2()
    ec2.stop_instance(instance_id)
    assert True

#testing describe instance
def test_describe_instance():
    ec2=EC2()
    ec2.describe_instance(instance_id)
    assert True
    
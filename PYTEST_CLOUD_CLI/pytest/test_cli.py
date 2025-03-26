import subprocess
import pytest
import os
import boto3
from botocore.exceptions import ClientError
import sys,os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'CLOUD_CLI'))

import pytest
from ec2 import EC2
from s3 import S3
from cli_argpar import aws_s3, aws_ec2

 
@pytest.fixture
def setup_environment():
    # Setup code to create necessary resources before tests
    # For example, create a test bucket or instance
    yield
    # Teardown code to clean up resources after tests
    # For example, delete the test bucket or instance
 
def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result
 
def test_create_s3_bucket(setup_environment):
    command = "python CLOUD_CLI/cli_argpar.py s3 create test-bucket"
    result = run_command(command)
    print(result.stdout)
    assert "Created bucket test-bucket" in result.stdout
 
def test_upload_file_to_s3(setup_environment):
    # Create a test file
    with open("test.txt", "w") as f:
        f.write(input("Enter some text: "))
   
    command = "python CLOUD_CLI/cli_argpar.py s3 upload test-bucket test.txt uploaded_test.txt"
    result = run_command(command)
    print(result.stdout)
    assert "Uploaded test.txt to test-bucket as uploaded_test.txt" in result.stdout
 
    # Clean up test file
    os.remove("test.txt")
    
 
def test_download_file_from_s3(setup_environment):
    with open("test.txt", "w") as f:
        f.write(input("Enter some text: "))
   
    command1 = "python CLOUD_CLI/cli_argpar.py s3 upload test-bucket test.txt uploaded_test.txt"
    result1 = run_command(command1)
    
    
    command2 = "python CLOUD_CLI/cli_argpar.py s3 download test-bucket test.txt uploaded_test.txt"
    result2 = run_command(command2)
    print(result2.stdout)
    assert "Downloaded uploaded_test.txt from test-bucket to test.txt" in result2.stdout
    # Clean up downloaded file
    os.remove("test.txt")
 
def test_describe_s3_buckets(setup_environment):
    with open("test.txt", "w") as f:
        f.write(input("Enter some text: "))
   
    command1 = "python CLOUD_CLI/cli_argpar.py s3 upload test-bucket test.txt uploaded_test.txt"
    result1 = run_command(command1)
    command = "python CLOUD_CLI/cli_argpar.py s3 describe test-bucket test.txt uploaded_test.txt"
    result = run_command(command)
    print(result.stdout)
    assert "uploaded_test.txt in bucket test-bucket" in result.stdout
    
    
def instance():
    command = "python CLOUD_CLI/cli_argpar.py ec2 create --image_id ami-123456 --instance_type t2.micro --key_name test-key"
    result = run_command(command)
    print(result.stdout) 
    return result.stdout.split()[2] 

def test_create_ec2_instance():
    command = "python CLOUD_CLI/cli_argpar.py ec2 create --image_id ami-123456 --instance_type t2.micro --key_name test-key"
    result = run_command(command)
    print(result.stdout) 
    return "Created instance" in result.stdout 

def test_start_ec2_instance():
    instanceid=instance()
    command = f"python CLOUD_CLI/cli_argpar.py ec2 start {instanceid}" 
    result = run_command(command)
    print(result.stdout)
    return f"Started instance {instanceid}" in result.stdout

def test_stop_ec2_instance(setup_environment):
    instanceid=instance()
    command = f"python CLOUD_CLI/cli_argpar.py ec2 stop {instanceid}"
    result = run_command(command)
    print(result.stdout)
    assert f"Stopped instance {instanceid}" in result.stdout

def test_describe_ec2_instance(setup_environment):
    instanceid=instance()
    command = f"python CLOUD_CLI/cli_argpar.py ec2 describe {instanceid}"
    result = run_command(command)
    print(result.stdout)
    assert f"Instance ID: {instanceid}" in result.stdout
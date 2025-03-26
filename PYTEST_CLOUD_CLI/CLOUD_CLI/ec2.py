import boto3
import logging
import argparse
from botocore.exceptions import ClientError
from moto import mock_aws

class EC2:
    def __init__(self, aws_endpoint_url='http://localhost:4566', aws_access_key_id='test', aws_secret_access_key='test', region_name='us-east-1'):
        self.ec2 = boto3.client('ec2',
                            endpoint_url=aws_endpoint_url,
                            aws_access_key_id=aws_access_key_id,
                            aws_secret_access_key=aws_secret_access_key,
                            region_name=region_name)

    # create instance
    @mock_aws
    def create_instance(self,image_id, instance_type, key_name):
        try:
            

            # Create an instance
            response = self.ec2.run_instances(
                ImageId=image_id,   #specifies amazon machine image ID
                InstanceType=instance_type,    #specifies instance type t2.micro
                KeyName=key_name,   #specifies name of key pair for SSH access
                MinCount=1,
                MaxCount=1
            )
            instance_id = response['Instances'][0]['InstanceId']    #extracts instance ID from response
            print(f"Created instance {instance_id}")
        except ClientError as e:
            logging.error(e)


    #start instance
    @mock_aws
    def start_instance(self,instance_id):
        try:
            self.ec2.start_instances(InstanceIds=[instance_id])  #calls the start_instace method on EC2 client
            print(f"Started instance {instance_id}")
        except ClientError as e:
            logging.error(e)


    #stop instance
    @mock_aws
    def stop_instance(self,instance_id):
        try:
            self.ec2.stop_instances(InstanceIds=[instance_id])  #calls stop_instace method on EC2 client
            print(f"Stopped instance {instance_id}")
        except ClientError as e:
            logging.error(e)



    #describe instance
    @mock_aws
    def describe_instance(self,instance_id):
        try:
            response = self.ec2.describe_instances(InstanceIds=[instance_id])    #calls describe_instance method on EC2 client
            for reservation in response['Reservations']:      #Iterates over the reservations in the response
                for instance in reservation['Instances']:        #Iterates over the instances in each reservation
                    print(f"Instance ID: {instance['InstanceId']}")
                    print(f"State: {instance['State']['Name']}")
                    print(f"Instance Type: {instance['InstanceType']}")
                    print(f"Public IP: {instance.get('PublicIpAddress', 'N/A')}")
                    print(f"Private IP: {instance['PrivateIpAddress']}")
        except ClientError as e:
            logging.error(e)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="EC2 Instance Operations")
    parser.add_argument("operation", choices=["create","start", "stop", "describe"], help="Operation to perform")
    parser.add_argument("--image_id", required=False, help="ID of the AMI")
    parser.add_argument("--instance_type", required=False, help="Type of the instance")
    parser.add_argument("--key_name", required=False, help="Name of the key pair")
    parser.add_argument("instance_id", nargs="?", help="ID of the EC2 instance")

    args = parser.parse_args()
    
    ec2=EC2()
    
    if args.operation == "create":
        if not all([args.image_id, args.instance_type, args.key_name]):
            parser.error("the following arguments are required for create: --image_id, --instance_type, --key_name")
        ec2.create_instance(args.image_id, args.instance_type, args.key_namep)
        print("created")
    elif args.operation == "start":
        ec2.start_instance(args.instance_id)
        print("started")
    elif args.operation == "stop":
        ec2.stop_instance(args.instance_id)
        print("stopped")
    elif args.operation == "describe":
        ec2.describe_instance(args.instance_id)
        print("described")
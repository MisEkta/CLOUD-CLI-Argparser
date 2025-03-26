import boto3
import logging
import argparse
from botocore.exceptions import ClientError
from botocore.client import Config
from s3 import S3
from ec2 import EC2
s3=S3()
ec2=EC2()
 
#AWS S3
def aws_s3(args):
    if args.operation == "create":      
        s3.create_bucket(args.bucket_name)
        print("created")
    if args.operation == "upload":
        s3.upload_file(args.bucket_name, args.file_name, args.object_name)
        print("uploaded")
    elif args.operation == "download":
        s3.download_file(args.bucket_name, args.object_name, args.file_name)
        print("downloaded")
    elif args.operation == "describe":
        s3.describe_file(args.bucket_name, args.object_name)
        print("described")
        
        
#AWS EC2
def aws_ec2(args):    
    if args.operation == "create":
        if not all([args.image_id, args.instance_type, args.key_name]):
            parser.error("the following arguments are required for create: --image_id, --instance_type, --key_name")
        ec2.create_instance(args.image_id, args.instance_type, args.key_name)
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AWS Operations")
    subparser=parser.add_subparsers(dest="service", help="Service to interact with")
    
    
    #S3
    s3_parser = subparser.add_parser("s3", help="S3 File Operations")
    s3_parser.add_argument("operation", choices=["create","upload", "download", "describe"], help="Operation to perform")
    s3_parser.add_argument("bucket_name", help="Name of the S3 bucket")
    s3_parser.add_argument("file_name", nargs='?', help="Name of the file")
    s3_parser.add_argument("object_name", nargs='?',help="Name of the object in S3")
    
    
    #EC2
    ec2_parser = subparser.add_parser("ec2", help="EC2 Instance Operations")
    ec2_parser.add_argument("operation", choices=["create","start", "stop", "describe"], help="Operation to perform")
    ec2_parser.add_argument("--image_id", required=False, help="ID of the AMI")
    ec2_parser.add_argument("--instance_type", required=False, help="Type of the instance")
    ec2_parser.add_argument("--key_name", required=False, help="Name of the key pair")
    ec2_parser.add_argument("instance_id", nargs="?", help="ID of the EC2 instance")

    args = parser.parse_args()
    if args.service == "s3":
        aws_s3(args)
    elif args.service == "ec2":
        aws_ec2(args)
    
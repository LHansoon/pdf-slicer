import boto3
import json
import uuid
import os

bucket = "hl-bkt"
region = "us-east-1"

filename = f"{str(uuid.uuid4())}.txt"
f = open(filename, "a")
f.write("see you tomorrow")
f.close()

session = boto3.Session(aws_access_key_id=os.environ['aws_access_key_id'],
                        aws_secret_access_key=os.environ['aws_secret_access_key'],
                        aws_session_token=os.environ['aws_session_token'])
s3 = session.resource('s3')
something = s3.Bucket(bucket).upload_file(filename, filename, ExtraArgs={'ACL':'public-read'})
print("sdf")
import boto3
import os
import time
import json

session = boto3.Session(aws_access_key_id=os.environ['aws_access_key_id'],
                        aws_secret_access_key=os.environ['aws_secret_access_key'],
                        aws_session_token=os.environ['aws_session_token'])

url = "https://sqs.us-east-1.amazonaws.com/323940432787/new-job-queue"

sqs_client = session.client("sqs", region_name="us-east-1")
for i in range(32, 50):
    message = {"mission-id": f"{i}", "configuration": f"something here {i}"}
    response = sqs_client.send_message(
        QueueUrl=url,
        MessageBody=json.dumps(message)
    )
    print(response)

import boto3
import os
import time
import json

session = boto3.Session(aws_access_key_id=os.environ['aws_access_key_id'],
                        aws_secret_access_key=os.environ['aws_secret_access_key'],
                        aws_session_token=os.environ['aws_session_token'])

db_client = session.resource("dynamodb", region_name="us-east-1")
table = db_client.Table('missions')
response = table.put_item(
    Item={
         "mission-id": "1",
         "info": {
             "configuration": "something here"
         }
     }
)
print(response)
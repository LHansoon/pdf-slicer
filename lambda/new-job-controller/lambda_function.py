import json
import boto3
import shortuuid
import time
import datetime
import requests
import os

db_client = boto3.resource("dynamodb", region_name="us-east-1")


def generate_mission_id():
    uuid = shortuuid.uuid()
    ts = time.time()
    time_stamp = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S')
    return f"{time_stamp}-{uuid}"


def lambda_handler(event, context):
    print(event)

    # mission_id = generate_mission_id()
    records = event["Records"]
    for record in records:
        data = record["body"]
        data = json.loads(data)
        table = db_client.Table('missions')

        response = table.put_item(
            Item={
                "mission-id": data["mission-params"]["mission-id"],
                "mission-status": "running",
                "additional-info": {
                    "mission-requester-email": data["mission-params"]["mission-requester-email"],
                    "mission-email-notification-requested": data["mission-params"]["mission-email-notification-requested"]
                }
            }
        )

        request_info = data
        print(request_info)
        # request_info["mission-params"]["mission-id"] = mission_id

        worker_ip = os.environ['worker_ip']
        r = requests.post(f"http://{worker_ip}/process-mission", json=request_info)
        print(r.content)

    return {
        'statusCode': 200,
        'body': "not much I can tell you, but we are sure that the mission has been received..."
    }

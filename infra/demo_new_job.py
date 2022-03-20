import boto3
import os
import json

session = boto3.Session(aws_access_key_id=os.environ['aws_access_key_id'],
                        aws_secret_access_key=os.environ['aws_secret_access_key'],
                        aws_session_token=os.environ['aws_session_token'])

url = "https://sqs.us-east-1.amazonaws.com/323940432787/new-job-controller"
sqs_client = session.client("sqs", region_name="us-east-1", endpoint_url="https://sqs.us-east-1.amazonaws.com")

message = {
    "mission-params": {
        "mission-requester-email": "somebody@gmail.com",
        "mission-email-notification-requested": False,
        "mission-file-list": [
            "Sample_1.pdf"
        ]
    },
    "split-params": {
        "Sample_1.pdf": [
            {"part-id": 0, "from": 1, "to": 2},
            {"part-id": 1, "from": 1, "to": 1}
        ]
    },
    "merge-params": [{
        "0": {
            "file-name": "Sample_1.pdf",
            "inner-merge-order": {
                "0": {"from": 1, "to": 2},
                "1": {"from": 1, "to": 1}
            }
        },
        "1": {
            "file-name": "Sample_1.pdf",
            "inner-merge-order": {
                "0": {"from": 1, "to": 1},
                "1": {"from": 1, "to": 1}
            }
        }
    }, {
        "0": {
            "file-name": "Sample_1.pdf",
            "inner-merge-order": {
                "0": {"from": 1, "to": 2},
                "1": {"from": 1, "to": 1}
            }
        },
        "1": {
            "file-name": "Sample_1.pdf",
            "inner-merge-order": {
                "0": {"from": 1, "to": 1},
                "1": {"from": 1, "to": 1}
            }
        }
    }]
}

sqs_client.send_message(
    QueueUrl=url,
    MessageBody=json.dumps(message)
)

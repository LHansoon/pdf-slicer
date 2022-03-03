import json
import boto3

db_client = boto3.resource("dynamodb", region_name="us-east-1")


def lambda_handler(event, context):
    print(event)
    data = event["Records"][0]["body"]
    data = json.loads(data)
    table = db_client.Table('missions')
    response = table.put_item(
        Item={
            "mission-id": data["mission-id"],
            "info": {
                "configuration": data["configuration"]
            }
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

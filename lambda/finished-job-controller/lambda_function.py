import json
import boto3
import os
import smtplib

from botocore.exceptions import ClientError

db_client = boto3.resource("dynamodb", region_name="us-east-1")


def get_secret():
    secret_name = "pdf/email"
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        raise e
    else:
        secret = None
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
        return secret


def send_email(user, pwd, recipient, subject, body):
    from_email = user
    to_email = recipient if isinstance(recipient, list) else [recipient]
    subject = subject
    text = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (from_email, ", ".join(to_email), subject, text)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(user, pwd)
        server.sendmail(from_email, to_email, message)
        server.close()
        print('successfully sent the mail')
    except:
        print("failed to send mail")


def lambda_handler(event, context):
    print(event)

    records = event["Records"]
    for record in records:
        data = record["body"]
        data = json.loads(data)
        table = db_client.Table('missions')

        mission_id = data["mission-id"]
        mission_status = data["mission-status"]

        table.update_item(
            Key={"mission-id": mission_id},
            UpdateExpression="set #colName = :s",
            ExpressionAttributeValues={':s': mission_status},
            ExpressionAttributeNames={"#colName": "mission-status"},
            ReturnValues="NONE"
        )

        response = table.get_item(Key={"mission-id": mission_id})["Item"]
        print(response)
        if response["additional-info"]["mission-email-notification-requested"] is True:
            recipient = response["additional-info"]["mission-requester-email"]

            print("getting creds")
            email_cred = get_secret()
            print("got it")

            if email_cred is None:
                return {
                    'statusCode': 500,
                    'body': "Cred error, not able to send email"
                }

            bucket = os.environ['bucket']
            dir = os.environ['dir']
            url = f"https://{bucket}.s3.amazonaws.com/{dir}{mission_id}/{mission_id}-result.zip"

            subject = "Your mission at email splitter has finished"
            body = f"Hello,\nHere is the download link for your files:\n{url}"

            email_cred = json.loads(email_cred)
            send_email(email_cred["username"], email_cred["password"], recipient, subject, body)

    return {
        'statusCode': 200,
        'body': "It means everything works fine! woohoo"
    }

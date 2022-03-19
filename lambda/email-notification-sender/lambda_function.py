import json
import smtplib

import boto3
from botocore.exceptions import ClientError


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
        get_secret_value_response = client.get_secret_value(SecretId = secret_name)
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
    email_cred = get_secret()

    if email_cred is None:
        return {
            'statusCode': 500,
            'body': "Cred error, not able to send email"
        }

    mission_id = event["mission_id"]
    bucket = event["bucket"]
    dir = event["dir"]
    url = f"https://{bucket}.s3.amazonaws.com/{dir}{mission_id}/{mission_id}-result.zip"

    recipient = event["recipient"]
    subject = "Your mission at email splitter has finished"
    body = f"Hello,\nHere is the download link for your files:\n{url}"

    email_cred = json.loads(email_cred)
    send_email(email_cred["username"], email_cred["password"], recipient, subject, body)

    return {
        'statusCode': 200,
        'body': "not much I can tell you, but we are sure that the mission has been received..."
    }

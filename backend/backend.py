import requests
from flask import Flask, request
import boto3
import json
import os

app = Flask(__name__)

# initialize the boto3 session
session = boto3.Session(aws_access_key_id=os.environ['aws_access_key_id'],
                        aws_secret_access_key=os.environ['aws_secret_access_key'],
                        aws_session_token=os.environ['aws_session_token'])

FILE_UPLOAD_LOC = "upload"
S3_BKT = "pdf-slicer"
S3_UPLOAD_TARGET = "source"


def get_session():
    return boto3.Session(aws_access_key_id=os.environ['aws_access_key_id'],
                         aws_secret_access_key=os.environ['aws_secret_access_key'],
                         aws_session_token=os.environ['aws_session_token'])

@app.route("/getresult", methods=["GET"])
def getresult():
    request_args = request.args
    try:
        mission_id = request_args["mission-id"]

        session = get_session()
        db = session.resource('dynamodb')
        table = db.Table('missions')
        response = table.get_item(Key={"mission-id": mission_id})
        status = response["Item"]["mission-status"]

        return {"mission-status": status, "request-status": "success", "Message": "request good"}, 200
    except KeyError:
        return {"request-status": "fail", "Message": "Key error, make sure correct arguments"}, 200


@app.route("/postrequest", methods=["POST"])
def postrequest():
    json_request = request.json
    try:
        text = json_request["text"]
        sleep_time = json_request["sleep"]

        return "haha"
    except Exception as e:
        return "something wrong with ethe stuff you typed in (`ヮ´ )σ`∀´) ﾟ∀ﾟ)σ"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)

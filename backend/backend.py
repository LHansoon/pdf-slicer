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

@app.route("/getresult", methods=["GET"])
def index():
    json_request = request.json

    try:
        mission_id = json_request["mission_id"]

        return "haha"
    except Exception as e:
        return "mission not exist pal ( ・_ゝ・)"


@app.route("/postrequest", methods=["POST"])
def index():
    json_request = request.json
    try:
        text = json_request["text"]
        sleep_time = json_request["sleep"]

        return "haha"
    except Exception as e:
        return "something wrong with ethe stuff you typed in (`ヮ´ )σ`∀´) ﾟ∀ﾟ)σ"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)

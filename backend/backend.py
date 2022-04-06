import boto3
import json
import os
import datetime
import time
import shortuuid
import shutil

from flask import Flask, request

from decorators import exception_holder
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}}, supports_credentials=True)

FILE_UPLOAD_LOC = "upload"
S3_BKT = "pdf-slicer"
S3_UPLOAD_TARGET = "source"

S3_DOWNLOAD_TARGET = "ready"


def get_session():
    return boto3.Session(aws_access_key_id=os.environ['aws_access_key_id'],
                         aws_secret_access_key=os.environ['aws_secret_access_key'],
                         aws_session_token=os.environ['aws_session_token'])

@exception_holder
@app.route("/getresult", methods=["GET"])
def get_result():
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
        return {"request-status": "creating", "Message": "Either you have a wrong key entered or the job is still creating"}, 200


@exception_holder
@app.route("/postrequest", methods=["POST"])
def post_request():
    json_request = request.json
    session = get_session()

    mission_id = json_request["mission-params"]["mission-id"]
    file_list = json_request["mission-params"]["mission-file-list"]
    uploaded_list = os.listdir(os.path.join(FILE_UPLOAD_LOC, mission_id))

    app.logger.info(f"{mission_id} - start processing mission")

    # check whether the file list matching the files uploaded.
    for file in file_list:
        if file not in uploaded_list:
            app.logger.info(f"{mission_id} - failed, list not matching")
            return {"request-status": "fail", "Message": "file list not matching uploaded files"}, 200

    s3_bkt = session.resource("s3").Bucket(S3_BKT)
    for file in file_list:
        curr_dir = os.path.join(FILE_UPLOAD_LOC, mission_id, file)
        dest_s3_path = os.path.join(S3_UPLOAD_TARGET, mission_id, file)
        app.logger.info(f"{mission_id} - uploading file: {curr_dir}")
        s3_bkt.upload_file(curr_dir, dest_s3_path)

    app.logger.info(f"{mission_id} - uploading finished, deleting dir")
    # shutil.rmtree(os.path.join(FILE_UPLOAD_LOC, mission_id))
    app.logger.info(f"{mission_id} - deleting finished")

    app.logger.info(f"{mission_id} - sending request to sqs")
    sqs_url = "https://sqs.us-east-1.amazonaws.com/323940432787/new-job-queue"
    sqs_client = session.client("sqs", region_name="us-east-1", endpoint_url="https://sqs.us-east-1.amazonaws.com")
    sqs_client.send_message(
        QueueUrl=sqs_url,
        MessageBody=json.dumps(json_request)
    )
    app.logger.info(f"{mission_id} - sqs mission created")
    return {"request-status": "success", "Message": "request good"}, 200


def generate_mission_id():
    uuid = shortuuid.uuid()
    ts = time.time()
    time_stamp = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S')
    return f"{time_stamp}-{uuid}"


@exception_holder
@app.route("/getmissionid", methods=["GET"])
def get_mission_id():
    mission_id = generate_mission_id()
    return {"mission-id": mission_id, "request-status": "success", "Message": "request good"}, 200

@exception_holder
@app.route("/getdownloadlink", methods=["GET"])
def get_mission_id():
    request_args = request.args

    try:
        mission_id = request_args["mission-id"]

        url = f"https://{S3_BKT}.s3.amazonaws.com/{S3_DOWNLOAD_TARGET}/{mission_id}/{mission_id}-result.zip"

        return {"download-link": url, "request-status": "success", "Message": "request good"}, 200
    except Exception:
        return {"request-status": "fail", "Message": "downloadlink generate failed"}, 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)

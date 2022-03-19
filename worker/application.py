import json
import threading
from flask import Flask, request
import decorators
import worker
import os
import boto3
import traceback


application = Flask(__name__)

logger = application.logger

file_dir = "./download_files"
finished_dir = "./finished_files"

s3_bkt = "pdf-slicer"
s3_source = "source"
s3_dest = "ready"
s3_merge_dir = "merge"
s3_split_dir = "split"

@application.before_first_request
def before_first_request():
    application.logger.info(f"===          First request received, welcome")
    application.logger.info(f"===          tmp download file dir is -> {file_dir}")
    application.logger.info(f"===          tmp finished file dir is -> {finished_dir}")

def execute_mission(json_request):
    global mission_id
    session = boto3.Session(aws_access_key_id=os.environ['aws_access_key_id'],
                            aws_secret_access_key=os.environ['aws_secret_access_key'],
                            aws_session_token=os.environ['aws_session_token'])
    message = {"mission-id": "", "status": "finished"}
    try:
        mission_params, split_job_params, merge_job_params = worker.parse_new_job_json(json_request)
        mission_id = mission_params["mission-id"]
        message["mission-id"] = mission_id
        worker.prepare_files(mission_id=mission_id,
                             s3_bkt=s3_bkt,
                             s3_dir=s3_source,
                             file_list=mission_params["mission-file-list"],
                             dest_dir=file_dir,
                             boto_session=session)

        mission = worker.Mission(mission_id=mission_id,
                                 split_params=split_job_params,
                                 merge_params=merge_job_params,
                                 boto_session=session,
                                 source_file_dir=os.path.join(file_dir, mission_id),
                                 dump_file_dir=finished_dir)

        mission.process_job()
        mission.upload_files(s3_bkt=s3_bkt,
                             s3_dest_dir=s3_dest)
    except Exception as e:
        application.logger.info(traceback.format_exc())
        message["status"] = "failed"
    finally:
        url = "https://sqs.us-east-1.amazonaws.com/323940432787/finished-job-queue"
        sqs_client = session.client("sqs", region_name="us-east-1", endpoint_url="https://sqs.us-east-1.amazonaws.com")
        sqs_client.send_message(
            QueueUrl=url,
            MessageBody=json.dumps(message)
        )
        if mission_id is not None:
            worker.clean_up(mission_id, os.path.join(file_dir, mission_id), finished_dir)

@application.route("/process-mission", methods=["POST"])
@decorators.router_wrapper
def start_mission():
    json_request = request.json
    json_request = json.dumps(json_request)

    t = threading.Thread(target=execute_mission, args=[json_request])
    t.setDaemon(False)
    t.start()

    return "mission received", 200

@application.route("/")
def default():
    return "hello budy"


@application.route("/healthCheck")
def eb_health_check():
    return "I am alive"

if __name__ == '__main__':
    application.run(host="0.0.0.0", port=8000, debug=True)

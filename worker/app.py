from flask import Flask, request
import decorators
import worker
import os
import boto3

app = Flask(__name__)

logger = app.logger

file_dir = "./download_files"
finished_dir = "./finished_files"


@app.before_first_request
def before_first_request():
    app.logger.info(f"===          First request received, welcome")
    app.logger.info(f"===          tmp download file dir is -> {file_dir}")
    app.logger.info(f"===          tmp finished file dir is -> {finished_dir}")


@app.route("/process-mission", methods=["POST"])
@decorators.router_wrapper
def start_mission():
    session = boto3.Session(aws_access_key_id=os.environ['aws_access_key_id'],
                            aws_secret_access_key=os.environ['aws_secret_access_key'],
                            aws_session_token=os.environ['aws_session_token'])
    json_request = request.json

    mission_params, split_job_params, merge_job_params = worker.parse_new_job_json(json_request, session)
    worker.prepare_files(mission_params["mission_id"], mission_params["file_list"], file_dir, session)

    mission = worker.Mission(mission_id=mission_params["mission_id"],
                             split_params=split_job_params,
                             merge_params=merge_job_params,
                             boto_session=session,
                             source_file_dir=file_dir,
                             dump_file_dir=finished_dir)

    merge_files = mission.process_merge()
    split_files = mission.process_split()

    files = merge_files + split_files
    return "", 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)

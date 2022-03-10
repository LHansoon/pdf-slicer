import boto3
import json
import uuid
import os

bucket = "hl-bkt"
region = "us-east-1"


file_config = {
    "bucket": "pdf-slicer",
    "source": "source",
    "dest": "ready"
}


def prepare_files(mission_id, file_list, dest_dir, boto_session):
    s3_bucket = boto_session.resource('s3').Bucket(file_config["bucket"])

    # create local folder for mission
    local_folder = f"{dest_dir}/{mission_id}"
    if not os.path.exists(local_folder):
        os.makedirs(local_folder)

    # download form s3
    for file in file_list:
        s3_file_dir = f"{file_config['source']}/{mission_id}/{file}"
        local_file_dir = f"{local_folder}/{file}"
        print(s3_file_dir)
        s3_bucket.download_file(s3_file_dir, local_file_dir)


session = boto3.Session(aws_access_key_id=os.environ['aws_access_key_id'],
                        aws_secret_access_key=os.environ['aws_secret_access_key'],
                        aws_session_token=os.environ['aws_session_token'])

prepare_files("asdfasdf-3e23423423423a-f2ef2ef2e23f", ["Sample_1.pdf"], "download", session)
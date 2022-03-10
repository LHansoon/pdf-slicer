import os

from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter
from flask import current_app as app
import json
import shortuuid
import boto3
import datetime
import time

import decorators


file_config = {
    "bucket": "pdf-slicer",
    "source": "source",
    "dest": "ready"
}


def get_random_pdf_name():
    uuid = shortuuid.uuid()
    ts = time.time()
    time_stamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H-%M-%S')
    return f"{time_stamp}-{uuid}.pdf"


def prepare_files(mission_id, file_list, dest_dir, boto_session):
    s3_bucket = boto_session.resource('s3').Bucket(file_config["bucket"])

    # create local folder for mission
    local_folder = f"f{dest_dir}/{mission_id}"
    if not os.path.exists(local_folder):
        os.makedirs(local_folder)

    # download form s3
    for file in file_list:
        s3_file_dir = f"{file_config['source']}/{mission_id}/{file}"
        local_file_dir = f"{local_folder}/{file}"
        s3_bucket.download_file(s3_file_dir, local_file_dir)


def parse_new_job_json(job_params, boto_session):
    pass


def cleanup(files):
    pass


class Mission(object):
    def __init__(self, mission_id, split_params, merge_params, boto_session, source_file_dir, dump_file_dir):
        self.mission_id = mission_id
        self.split_params = split_params
        self.merge_params = merge_params
        self.boto_session = boto_session
        self.source_file_dir = source_file_dir
        self.dump_file_dir = dump_file_dir


    def process_split(self):
        pass

    def process_merge(self):
        pass

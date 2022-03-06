from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter
from flask import current_app as app
import json
import shortuuid
import boto3
import datetime
import time

import decorators


def get_random_pdf_name():
    uuid = shortuuid.uuid()
    ts = time.time()
    time_stamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H-%M-%S')
    return f"{time_stamp}-{uuid}.pdf"


def prepare_files(file_list, dest_dir, boto_session):


    pass


def job_prepare(job_params, boto_session):
    pass


def cleanup(files):
    pass


class Mission(object):
    def __init__(self, split_params, merge_params, boto_session, source_file_dir, dump_file_dir):
        self.split_params = split_params
        self.merge_params = merge_params
        self.boto_session = boto_session
        self.source_file_dir = source_file_dir
        self.dump_file_dir = dump_file_dir

    def process_split(self):
        pass

    def process_merge(self):
        pass

import os

from pikepdf import Pdf as PDF
from flask import current_app as app
import json
import shortuuid
import boto3
import datetime
import time

import decorators

file_config = {
    "bucket": "pdf-slicer",
    "s3_source": "source",
    "dest": "ready",
    "dest_split": "split",
    "dest_merge": "merge"
}


def get_random_pdf_name():
    uuid = shortuuid.uuid()
    ts = time.time()
    time_stamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H-%M-%S')
    return f"{time_stamp}-{uuid}.pdf"


def parse_new_job_json(job_params):
    params = json.loads(job_params)
    mission_params = params["mission-params"]
    split_job_params = params["split-params"]
    merge_job_params = params["merge-params"]
    return mission_params, split_job_params, merge_job_params


def mkdir_if_not_exist(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)


def prepare_files(mission_id, file_list, dest_dir, boto_session):
    s3_bucket = boto_session.resource('s3').Bucket(file_config["bucket"])

    # create local folder for mission
    local_folder = os.path.join(dest_dir, mission_id)
    mkdir_if_not_exist(local_folder)

    # download form s3
    for file in file_list:
        s3_file_dir = os.path.join(file_config['s3_source'], mission_id, file)
        local_file_dir = os.path.join(local_folder, file)
        if not os.path.exists(local_file_dir):
            s3_bucket.download_file(s3_file_dir, local_file_dir)


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
        mkdir_if_not_exist(self.dump_file_dir)

    def process_job(self):
        split_files = self.process_split()
        merge_files = self.process_merge()

    def __split_file(self, source_file_dir: str, result_file_name, result_file_dir, pg_from, pg_to):
        app.logger.info(f"New Split Mission\n"
                        f"\t==>source_dir: {source_file_dir}\n"
                        f"\t==>result file name: {result_file_name}\n"
                        f"\t==>page from: {pg_from}\t page to: {pg_to}")

        dest_file_dir = os.path.join(result_file_dir, result_file_name)
        pg_from -= 1
        pg_to -= 1

        source_pdf = PDF.open(source_file_dir)
        dest_pdf = PDF.new()
        for pg_num in range(pg_from, pg_to + 1):
            page = source_pdf.pages[pg_num]
            dest_pdf.pages.append(page)
        dest_pdf.save(dest_file_dir)

    def process_split(self):
        # prepare mission split dir
        target_dir = os.path.join(self.dump_file_dir, file_config["dest_split"], self.mission_id)
        mkdir_if_not_exist(target_dir)
        # iter through all the files need to be split on list
        for file_name, split_params in self.split_params.items():
            source_file_dir = os.path.join(self.source_file_dir, file_name)
            for split_param in split_params:
                slice_id = split_param["part-id"]
                page_from = split_param["from"]
                page_to = split_param["to"]
                splitted_file_name = f"file_No_{slice_id}_pg{page_from}-{page_to}.pdf"
                self.__split_file(source_file_dir, splitted_file_name, target_dir, page_from, page_to)

    def process_merge(self):
        target_dir = os.path.join(self.dump_file_dir, file_config["dest_merge"], self.mission_id)
        mkdir_if_not_exist(target_dir)

        keys = self.merge_params.keys()
        max_key = int(max(keys))

        dest_pdf = PDF.new()
        for number in range(max_key + 1):
            slice_params = self.merge_params[f"{number}"]
            file_name = slice_params["file-name"]
            source_file_dir = os.path.join(self.source_file_dir, file_name)
            source_pdf = PDF.open(source_file_dir)

            segments = []
            for segment_key in slice_params["inner-merge-order"].keys():
                segment_pages = []
                segment_params = slice_params["inner-merge-order"][segment_key]
                pg_from = segment_params["from"]
                pg_to = segment_params["to"]
                for pg_num in range(pg_from, pg_to + 1):
                    page = source_pdf.pages[pg_num - 1]
                    segment_pages.append(page)
                segments.insert(int(segment_key), segment_pages)

            for segment in segments:
                for page in segment:
                    dest_pdf.pages.append(page)

        file_name = f"merged-{self.mission_id}.pdf"
        target_file_dir = os.path.join(target_dir, file_name)
        dest_pdf.save(target_file_dir)

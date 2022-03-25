import os, psutil

import pikepdf
from pikepdf import Pdf as PDF
import application as current_app
import json
import shortuuid
import datetime
import time
import shutil

# this is pymupdf
import fitz

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


def logging_mission(tag, text):
    current_ram = round(psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2, 2)
    current_ram_percen = round(psutil.virtual_memory().available * 100 / psutil.virtual_memory().total, 2)
    current_cpu_percen = round(psutil.cpu_percent(), 2)
    current_app.logger.info(f"cpu: {current_cpu_percen}% \tram: {current_ram} \t{current_ram_percen}% {tag} -- {text}")


def prepare_files(mission_id, s3_bkt, s3_dir, file_list, dest_dir, boto_session):
    logging_mission(mission_id, f"preparing file for mission")
    s3_bucket = boto_session.resource('s3').Bucket(s3_bkt)

    # create local folder for mission
    local_folder = os.path.join(dest_dir, mission_id)
    mkdir_if_not_exist(local_folder)

    # download form s3
    for file in file_list:
        s3_file_dir = os.path.join(s3_dir, mission_id, file)
        local_file_dir = os.path.join(local_folder, file)
        if not os.path.exists(local_file_dir):
            s3_bucket.download_file(s3_file_dir, local_file_dir)
    logging_mission(mission_id, f"preparing file for mission finished")


class Mission(object):
    def __init__(self, mission_id, translate_params, split_params, merge_params, boto_session, source_file_dir, dump_file_dir):
        self.mission_id = mission_id
        self.translate_params = translate_params
        self.split_params = split_params
        self.merge_params = merge_params
        self.boto_session = boto_session
        self.source_file_dir = source_file_dir
        self.dump_file_dir = dump_file_dir
        mkdir_if_not_exist(self.dump_file_dir)

    def upload_files(self, s3_bkt, s3_dest_dir):
        logging_mission(self.mission_id, "start uploading files")
        s3_bkt = self.boto_session.resource("s3").Bucket(s3_bkt)
        result_dir = os.path.join(self.dump_file_dir, self.mission_id)

        zip_name = f"{self.mission_id}-result"
        zip_dir = os.path.join(self.dump_file_dir, zip_name)
        shutil.make_archive(zip_dir, 'zip', result_dir)
        zip_dir += ".zip"
        zip_name += ".zip"
        s3_path = os.path.join(s3_dest_dir, self.mission_id, zip_name)
        s3_bkt.upload_file(zip_dir, s3_path)
        os.remove(zip_dir)

        logging_mission(self.mission_id, "file uploading finished")

    def process_job(self):
        logging_mission(self.mission_id, f"mission started")
        self.process_split()
        self.process_merge()
        if self.translate_params["if_translate"]:
            self.process_translate()
        logging_mission(self.mission_id, f"mission finished")

    def __split_file(self, source_file_dir: str, result_file_name, result_file_dir, pg_from, pg_to):
        dest_file_dir = os.path.join(result_file_dir, result_file_name)
        pg_from -= 1
        pg_to -= 1

        source_pdf = PDF.open(source_file_dir)
        dest_pdf = PDF.new()
        for pg_num in range(pg_from, pg_to + 1):
            page = source_pdf.pages[pg_num]
            dest_pdf.pages.append(page)
        dest_pdf.save(dest_file_dir)

    def process_translate(self):
        logging_mission(self.mission_id, f"translation job started")
        source_dir = os.path.join(self.dump_file_dir, self.mission_id)

        translate = self.boto_session.client('translate')

        for root, dirs, files in os.walk(source_dir):
            for file in files:
                path = os.path.join(source_dir, str(file))
                filename, file_extension = os.path.splitext(file)
                target_language = self.translate_params["target_language"]
                source_language = self.translate_params["source_language"]
                translated_file_name = os.path.join(source_dir, str(filename) + f"_{target_language}.txt")

                logging_mission(self.mission_id, f"working on: {translated_file_name}")

                target_file = open(translated_file_name, "a")
                with fitz.Document(path) as original:
                    i = 1
                    for page in original:
                        page_text = page.get_text()
                        result = translate.translate_text(Text=page_text,
                                                 SourceLanguageCode=source_language,
                                                 TargetLanguageCode=target_language)
                        target_file.write(f"===page {i}===\n")
                        target_file.write(result["TranslatedText"])
                        i += 1
                target_file.close()

        logging_mission(self.mission_id, f"translation job finished")

    def process_split(self):
        logging_mission(self.mission_id, f"splitting job start")
        # prepare mission split dir
        target_dir = os.path.join(self.dump_file_dir, self.mission_id)
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
        logging_mission(self.mission_id, f"splitting job finished")

    def process_merge(self):
        logging_mission(self.mission_id, f"merging job start")
        target_dir = os.path.join(self.dump_file_dir, self.mission_id)
        mkdir_if_not_exist(target_dir)

        i = 1
        for merge_job in self.merge_params:
            keys = merge_job.keys()
            max_key = int(max(keys))

            dest_pdf = PDF.new()
            for number in range(max_key + 1):
                slice_params = merge_job[f"{number}"]
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

            file_name = f"merged-mission-{i}-{self.mission_id}.pdf"
            target_file_dir = os.path.join(target_dir, file_name)
            dest_pdf.save(target_file_dir)
            logging_mission(self.mission_id, f"merging job finished")
            i += 1


def clean_up(mission_id, source_file_dir, dump_file_dir):
    logging_mission(mission_id, f"cleaning up mission")
    dir_list = [os.path.join(dump_file_dir, mission_id),
                source_file_dir]

    for dir in dir_list:
        for root, dirs, files in os.walk(dir):
            for file in files:
                path = os.path.join(dir, file)
                if os.path.exists(path):
                    os.remove(path)
        if os.path.exists(dir):
            os.rmdir(dir)

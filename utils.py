# -*- coding: utf-8 -*-
import gzip
import json
import os
import shutil
from pathlib import Path

src_path = Path(os.path.dirname(os.path.realpath(__file__)))
root_path = src_path.absolute()
input_path = os.path.join(root_path, "inputs")
input_datatable_path = os.path.join(input_path, "datatable")
inject_datatable_path = os.path.join(input_datatable_path, "inject")
extract_datatable_path = os.path.join(input_datatable_path, "extract")
output_path = os.path.join(root_path, "outputs")
output_datatable_path = os.path.join(output_path, "datatable")
music_ai_section_filename = "music_ai_section.bin"
music_attribute_filename = "music_attribute.bin"
music_order_filename = "music_order.bin"
musicinfo_filename = "musicinfo.bin"
wordlist_filename = "wordlist.bin"
datatable_filenames = [music_ai_section_filename, music_attribute_filename, music_order_filename, musicinfo_filename,
                       wordlist_filename]
inject_datatable_filepaths = [os.path.join(inject_datatable_path, filename) for filename in datatable_filenames]
extract_datatable_filepaths = [os.path.join(extract_datatable_path, filename) for filename in datatable_filenames]
output_datatable_filepaths = [os.path.join(output_datatable_path, filename) for filename in datatable_filenames]


def read_json(json_path: str) -> dict:
    with open(json_path) as f:
        data = json.load(f)
    return data


def get_datatable_files() -> tuple[list, list]:
    inject_data_list = []
    extract_data_list = []
    for filepath in inject_datatable_filepaths:
        with open(filepath, "rb") as f:
            json_data = json.loads(gzip.decompress(f.read()).decode("utf-8"))["items"]
        inject_data_list.append(json_data)
    for filepath in extract_datatable_filepaths:
        with open(filepath, "rb") as f:
            json_data = json.loads(gzip.decompress(f.read()).decode("utf-8"))["items"]
        extract_data_list.append(json_data)
    return inject_data_list, extract_data_list


def write_datatable_files(data_list: tuple) -> None:
    for filepath, data in zip(output_datatable_filepaths, data_list):
        with open(filepath, "wb") as f:
            f.write(gzip.compress(
                json.dumps({"items": data}, sort_keys=True, indent="\t", ensure_ascii=False).encode("utf-8")))


def find_cur_dir() -> str:
    return os.getcwd()


def make_dir(path: str) -> None:
    if not os.path.exists(path):
        os.makedirs(path)


def enumerate_files(path: str) -> tuple[list, list]:
    output_filepaths = []
    output_filenames = []
    for root, folder, filenames in os.walk(path):
        for filename in filenames:
            output_filepaths.append(os.path.join(root, filename))
            output_filenames.append(filename)
    return output_filepaths, output_filenames


def remove_dir(path: str) -> None:
    if os.path.exists(path):
        shutil.rmtree(path)


def init() -> None:
    remove_dir(output_path)
    for path in [input_path, output_path, input_datatable_path, inject_datatable_path, extract_datatable_path,
                 output_datatable_path]:
        make_dir(path)
    for filepath in inject_datatable_filepaths:
        if not os.path.exists(filepath):
            print("%s" % filepath + " not found.\n")
            input("Press Enter to exit...")
            exit()
    for filepath in extract_datatable_filepaths:
        if not os.path.exists(filepath):
            print("%s" % filepath + " not found.\n")
            input("Press Enter to exit...")
            exit()


def copy_file(src: str, dst: str) -> None:
    if os.path.exists(dst):
        os.remove(dst)
    if not os.path.exists(src):
        return
    if not os.path.exists(os.path.dirname(dst)):
        os.makedirs(os.path.dirname(dst))
    shutil.copy(src, dst)

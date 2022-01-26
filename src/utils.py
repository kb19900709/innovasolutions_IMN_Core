import json
import os
from json import JSONDecodeError

SOURCE_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCES_DIR = os.path.join(SOURCE_ROOT_DIR, '../resources/')


def get_json_list_by_file(file_name: str):
    try:
        return json.load(open(RESOURCES_DIR + file_name))
    except JSONDecodeError as err:
        print(f"error occurs while parsing json file. {err}")
        raise
    except FileNotFoundError as err:
        print(f"file not found, please check the data path. {err}")
        raise

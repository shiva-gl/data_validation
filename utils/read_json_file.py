import json


def read_json_file_to_dict():
    return json.load(open('./sql_queries_info.json'))

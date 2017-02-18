import os
import sys
import json


def open_file_as_string(filepath):
    with open(filepath, 'r') as ftemp:
        templateString = ftemp.read()
    return templateString


def return_absolut_path(script_path, relative_path):
    return os.path.realpath(os.path.join(script_path, relative_path))


def fetch_json_file_as_dict(path_to_json):
    #db_schema_path = return_absolut_path(script_path, relative_path)
    json_str = open_file_as_string(path_to_json)
    json_dict = json.loads(json_str)
    return json_dict





if __name__ == '__main__':
    unittest.main()

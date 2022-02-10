import json


class Reading:
    @staticmethod
    def read_json(path):
        with open(path, 'r') as json_file:
            return json.load(json_file)

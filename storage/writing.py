import json


class Writing:
    @staticmethod
    def write_json(path, data):
        with open(path, 'w') as json_file:
            json.dump(data, json_file)

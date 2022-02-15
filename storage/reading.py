import json


# CR: Reader. class name shouldn't be a verb
class Reading:
    @staticmethod
    def read_json(path):
        with open(path, 'r') as json_file:
            return json.load(json_file)

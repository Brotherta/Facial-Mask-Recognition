import json


class Label:

    def __init__(self, name):
        self.name = name


class LabelEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__

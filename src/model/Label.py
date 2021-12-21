import json


class Label:

    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return other.name == self.name


class LabelEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__

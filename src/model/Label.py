import json

# The label model. Contains just the string value of the name
class Label:

    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        """ Redefine equals operator """
        return other.name == self.name


# Allows the json encode
class LabelEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__

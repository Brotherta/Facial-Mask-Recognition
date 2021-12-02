import configparser
import os


class Project:

    def __init__(self, name, filepath):
        self.name = name
        self.path = filepath
        self.config = configparser.ConfigParser()

    def create_config(self):
        self.config['PROJECT'] = {
            'name': self.name,
            'filepath': self.path,
            'labels': self.path+"/labels.json",
            'images': self.path+"/images"
        }
        with open(self.path+"/project.ini", 'w') as f:
            self.config.write(f)

        with open(self.path+"/labels.json", 'w') as f:
            f.write("{}")

        try:
            os.mkdir(self.path + "/images")
        except Exception as e:
            print(e)


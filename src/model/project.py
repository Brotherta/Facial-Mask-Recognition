import configparser
import json
import os


class Project:

    def __init__(self, name, filepath):
        self.name = name
        self.path = filepath
        self.config_path = filepath+'/project.ini'
        self.labels_path = filepath+'/labels.json'
        self.config = configparser.ConfigParser()

    def create_config(self):
        self.config['PROJECT'] = {
            'name': self.name,
            'filepath': self.path,
            'labels': self.path+"/labels.json",
            'images': self.path+"/images"
        }
        with open(self.config_path, 'w') as f:
            self.config.write(f)


        with open(self.labels_path, 'w') as f:
            f.write("{}")
            f.flush()
            f.close()

        try:
            os.mkdir(self.path + "/images")
        except Exception as e:
            print(e)

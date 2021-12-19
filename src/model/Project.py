import configparser
import json
import os
import shutil
from types import SimpleNamespace

from src.data.DataContainer import DataContainer
from src.model.Box import Box
from src.model.ImageFMR import ImageFMR, ImageFMREncoder
from src.model.Label import Label, LabelEncoder


class Project:

    def __init__(self, name, folder_path):
        self.name = name
        self.path = folder_path
        self.configPath = folder_path + '/project.ini'
        self.imagesPath = folder_path + "/images"
        self.labelsPath = folder_path + '/labels.json'
        self.boxPath = folder_path + '/box.json'
        self.config = configparser.ConfigParser()
        self.concatenatedSaves = ""

    def loadProject(self, data: DataContainer):
        data.project = self
        if os.path.isfile(self.labelsPath):
            with open(self.labelsPath, 'r') as f:
                labels = json.loads(f.read(), object_hook=lambda d: SimpleNamespace(**d))
                final_labels = list(map(lambda x: Label(x.name), labels))
                data.labels = final_labels
                f.flush()
                f.close()

        if os.path.isfile(self.boxPath):
            try:
                with open(self.boxPath, 'r') as f:
                    images = json.loads(f.read(), object_hook=lambda d: SimpleNamespace(**d))
                    finalImages = []
                    for i in images:
                        boxList = []
                        for box in i.boxList:
                            boxList.append(Box(box.x, box.y, box.width, box.height, box.label))

                        finalImages.append(ImageFMR(i.filepath, boxList, i.imageSize))
                    data.images = finalImages

            except json.JSONDecodeError as e:
                with open(self.boxPath, 'w') as f:
                    f.seek(0)
                    f.write('[]')
                    f.truncate()
            dumpedLabels = json.dumps(data.labels, indent=4, cls=LabelEncoder)
            dumpedImages = json.dumps(data.images, indent=4, cls=LabelEncoder)
            self.concatenatedSaves = dumpedLabels + dumpedImages


    def saveProject(self, data: DataContainer):
        labels = data.labels
        images = data.images
        dumpedLabels = json.dumps(labels, indent=4, cls=LabelEncoder)
        dumpedImages = json.dumps(images, indent=4, cls=LabelEncoder)
        with open(self.labelsPath, 'w') as f:
            f.write(dumpedLabels)
            f.flush()
            f.close()
        with open(self.boxPath, 'w') as f:
            f.write(dumpedImages)
            f.flush()
            f.close()
        self.concatenatedSaves = dumpedLabels + dumpedImages

    def createConfig(self):
        """ Create a new config file for the project """
        self.config['PROJECT'] = {
            'name': self.name,
            'filepath': self.path,
            'labels': self.labelsPath,
            'box': self.boxPath,
            'images': self.imagesPath
        }
        with open(self.configPath, 'w') as f:
            self.config.write(f)

        if not os.path.isfile(self.labelsPath):
            with open(self.labelsPath, 'w') as f:
                f.write("[]")
                f.flush()
                f.close()

        if not os.path.isfile(self.boxPath):
            with open(self.boxPath, 'w') as f:
                f.write("[]")
                f.flush()
                f.close()

        try:
            os.mkdir(self.path + "/images")
        except Exception as e:
            print(e)

    def saveConfig(self):
        """ Save into projects.json the config of the project """
        try:
            with open('projects.json', 'a+') as f:
                oldConfig = json.load(f)
                f.flush()
                f.close()
        except json.JSONDecodeError:
            oldConfig = {"projects": []}

        oldConfig['projects'].append(self.configPath)

        with open('projects.json', 'w') as f:
            f.seek(0)
            f.write(json.dumps(oldConfig, sort_keys=True, indent=4))
            f.truncate()
            f.flush()
            f.close()

    def delete(self):
        """ Delete from projects.json, the path of the current project. """
        with open('projects.json', 'r') as f:
            config = json.load(f)
            f.close()
        config['projects'].remove(self.configPath)
        with open('projects.json', 'w') as f:
            f.seek(0)
            f.write(json.dumps(config, sort_keys=True, indent=4))
            f.close()

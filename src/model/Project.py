import configparser
import json
import os
from types import SimpleNamespace

from src.data.DataContainer import DataContainer
from src.model.Box import Box
from src.model.ImageFMR import ImageFMR
from src.model.Label import Label, LabelEncoder


# The project contain the project data.
# Load from each data in their json associated
class Project:

    def __init__(self, name, folder_path):
        self.name = name
        self.path = folder_path

        self.configPath = folder_path + '/project.ini'  # Project configuration file
        self.imagesPath = folder_path + "/images"  # Project images folder
        self.labelsPath = folder_path + '/labels.json'  # Labels json file
        self.boxPath = folder_path + '/box.json'  # The boxes json file
        self.config = configparser.ConfigParser()  # Parser of the project configuration file

        # This value concatenate images and labels save into a single variable. Like a hash function.
        # Briefly, it allows us to compare two different (self.data + self.labels) values.
        # This is very helpful to check if the user has already saved his data.
        # So this value is the initial loaded data state. And we will compare it to another state later.
        self.concatenatedSaves = ""

    def loadProject(self, data: DataContainer):
        """ Load the project from the files and put all data into the given DataContainer. """
        data.project = self

        # Labels part
        if os.path.isfile(self.labelsPath):  # If the labels json file exists
            with open(self.labelsPath, 'r') as f:  # Open the file
                # Parse the json data into SimpleNamespace objects SimpleNamespace allows us to
                # to parse objects into json and vice versa, but the parsed data is not usable.
                # So we convert the data to an usable state.
                labels = json.loads(f.read(), object_hook=lambda d: SimpleNamespace(**d))
                final_labels = list(map(lambda x: Label(x.name), labels))  # Parse correctly
                data.labels = final_labels  # Assigns the labels data to the data container
                f.flush()
                f.close()

        # Images part. The process is exactly the same as above
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
                    data.images = finalImages  # Assigns the images data to the data container

            # If there is an error, we recreate the file with an empty list
            except json.JSONDecodeError as e:
                with open(self.boxPath, 'w') as f:
                    f.seek(0)
                    f.write('[]')
                    f.truncate()
            dumpedLabels = json.dumps(data.labels, indent=4, cls=LabelEncoder)
            dumpedImages = json.dumps(data.images, indent=4, cls=LabelEncoder)
            self.concatenatedSaves = dumpedLabels + dumpedImages  # Set the initial data hash state. See constructor

    def saveProjectLabels(self, data: DataContainer):
        """ Write data.labels into the labels json file. """
        dumpedLabels = json.dumps(data.labels, indent=4, cls=LabelEncoder)  # Parse data.labels into json string
        with open(self.labelsPath, 'w') as f:
            f.write(dumpedLabels)  # Write data
            f.flush()
            f.close()

    def saveProjectImages(self, data: DataContainer):
        """ Write data.images into the images json file. """
        dumpedImages = json.dumps(data.images, indent=4, cls=LabelEncoder)  # Parse data.images into json string
        with open(self.boxPath, 'w') as f:
            f.write(dumpedImages)  # Write data
            f.flush()
            f.close()

    def saveProject(self, data: DataContainer):
        """ Save data.images and data.labels into their respectives files. """
        self.saveProjectLabels(data)
        self.saveProjectImages(data)

        dumpedLabels = json.dumps(data.labels, indent=4, cls=LabelEncoder)
        dumpedImages = json.dumps(data.images, indent=4, cls=LabelEncoder)
        self.concatenatedSaves = dumpedLabels + dumpedImages  # Create the hash

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
            self.config.write(f)  # Write the configuration file

        # Create the labels json file
        if not os.path.isfile(self.labelsPath):
            with open(self.labelsPath, 'w') as f:
                f.write("[]")  # Firstly, an empty list
                f.flush()
                f.close()

        # Create the boxes json file
        if not os.path.isfile(self.boxPath):
            with open(self.boxPath, 'w') as f:
                f.write("[]")  # Firstly, an empty list
                f.flush()
                f.close()

        try:
            os.mkdir(self.path + "/images")  # Create the images folder.
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

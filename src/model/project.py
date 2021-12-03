import configparser
import json
import os
from types import SimpleNamespace

from src.model.image_fmr import ImageFMR, ImageFMREncoder
from src.model.label import Label, LabelEncoder


class Project:

    def __init__(self, name, folder_path):
        self.name = name
        self.path = folder_path
        self.config_path = folder_path + '/project.ini'
        self.images_path = folder_path + "/images"
        self.labels_path = folder_path + '/labels.json'
        self.box_path = folder_path + '/box.json'
        self.config = configparser.ConfigParser()

    def create_config(self):
        self.config['PROJECT'] = {
            'name': self.name,
            'filepath': self.path,
            'labels': self.labels_path,
            'box': self.box_path,
            'images': self.images_path
        }
        with open(self.config_path, 'w') as f:
            self.config.write(f)

        if not os.path.isfile(self.labels_path):
            with open(self.labels_path, 'w') as f:
                f.write("[]")
                f.flush()
                f.close()

        if not os.path.isfile(self.box_path):
            with open(self.box_path, 'w') as f:
                f.write("[]")
                f.flush()
                f.close()

        try:
            os.mkdir(self.path + "/images")
        except Exception as e:
            print(e)

    def load_labels(self):
        if os.path.isfile(self.labels_path):
            with open(self.labels_path, 'r') as f:
                labels = json.loads(f.read(), object_hook=lambda d: SimpleNamespace(**d))
                final_labels = list(map(lambda x: Label(x.name), labels))
                return final_labels
        return []

    def save_labels(self, labels: list[Label]):
        with open(self.labels_path, 'w') as f:
            f.write(json.dumps(labels, indent=4, cls=LabelEncoder))
            f.flush()
            f.close()

    def load_images(self):
        if os.path.isfile(self.box_path):
            with open(self.box_path, 'r') as f:
                images = json.loads(f.read(), object_hook=lambda d: SimpleNamespace(**d))
                final_images = []
                for i in images:
                    boxs = []
                    for b in i.boxs:
                        # boxs.append(Box(QRect(b.rect[0], b.rect[1], b.rect[2], b.rect[3]), b.label))
                        pass
                    final_images.append(ImageFMR(i.filepath, boxs))
                return final_images
        return []

    def save_images(self, images: list[ImageFMR]):
        with open(self.box_path, 'w') as f:
            f.write(json.dumps(images, indent=4, cls=ImageFMREncoder))
            f.flush()
            f.close()

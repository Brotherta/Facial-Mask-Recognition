import json

import PIL
from PIL.ImageQt import ImageQt
from PyQt5.QtGui import QPixmap, QIcon

from src.model.Box import Box

MAX_IMAGE_SIZE = (1200, 675)


class ImageFMR:

    def __init__(self, filepath: str, boxList: list[Box] = [], imageSize: (int, int) = (0, 0)):
        self.filepath = filepath
        self.boxList: list[Box] = boxList
        self.imageSize = imageSize

    def toPixmap(self) -> QPixmap:
        image = PIL.Image.open(self.filepath).convert("RGBA")
        self.imageSize = (image.width, image.height)
        return QPixmap.fromImage(ImageQt(image))

    def toIcon(self) -> QIcon:
        return QIcon(self.filepath)

    @staticmethod
    def resizeImage(image):
        if image.width > 1600 or image.height > 900:
            image.thumbnail(MAX_IMAGE_SIZE)

    def addBox(self, box: Box):
        self.boxList.append(box)


class ImageFMREncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__

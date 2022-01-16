import json

import PIL
from PIL.ImageQt import ImageQt
from PyQt5.QtGui import QPixmap, QIcon

from src.model.Box import Box

MAX_IMAGE_SIZE = (1200, 675)


# Our model for images. This class contains the filepath, the boxes list of the images and the size.
# There is method to load the image into pixmap or icon.
class ImageFMR:

    def __init__(self, filepath: str, boxList: list[Box] = [], imageSize: (int, int) = (0, 0)):
        self.filepath = filepath
        self.boxList: list[Box] = boxList
        self.imageSize = imageSize

    def toPixmap(self) -> QPixmap:
        """ Load the image from the filepath into QPixmap. """
        image = PIL.Image.open(self.filepath).convert("RGBA")
        self.imageSize = (image.width, image.height)
        return QPixmap.fromImage(ImageQt(image))

    def toIcon(self) -> QIcon:
        """ Load the image from the filepath into QIcon. """
        return QIcon(self.filepath)

    @staticmethod
    def resizeImage(image):
        """ Resize the image if needed (too big). """
        if image.width > MAX_IMAGE_SIZE[0] or image.height > MAX_IMAGE_SIZE[1]:
            image.thumbnail(MAX_IMAGE_SIZE)

    def addBox(self, box: Box):
        """ Assign a box to the image. """
        self.boxList.append(box)


# Allows the json encode
class ImageFMREncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__

import PIL
from PIL.ImageQt import ImageQt
from PyQt5.QtGui import QPixmap, QIcon

from src.model.box import Box

MAX_IMAGE_SIZE = (1600, 900)


class ImageFMR:

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.boxs = []

    def to_pixmap(self) -> QPixmap:
        image = PIL.Image.open(self.filepath).convert("RGBA")
        self.resize_image(image)
        return QPixmap.fromImage(ImageQt(image))

    def to_icon(self) -> QIcon:
        return QIcon(self.filepath)

    def resize_image(self, image):
        if image.width > 1600 or image.height > 900:
            image.thumbnail(MAX_IMAGE_SIZE)

    def add_box(self, box: Box):
        self.boxs.append(box)

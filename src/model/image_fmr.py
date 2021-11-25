import PIL.Image
from PIL.ImageQt import ImageQt
from PyQt5.QtGui import QPixmap

MAX_IMAGE_SIZE = (1600, 900)


class ImageFMR:
    image: PIL.Image
    filepath: str

    def __init__(self, filepath: str):
        self.image = PIL.Image.open(filepath)
        self.image = self.image.convert("RGBA")
        self.resize_image()

    def to_pixmap(self) -> QPixmap:
        pix = QPixmap.fromImage(ImageQt(self.image))
        return pix

    def resize_image(self):
        if self.image.width > 1600 or self.image.height > 900:
            self.image.thumbnail(MAX_IMAGE_SIZE)

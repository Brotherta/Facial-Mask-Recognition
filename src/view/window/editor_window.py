import PIL
from PIL.ImageQt import ImageQt
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QDialog, QInputDialog, QPushButton, QVBoxLayout, QMessageBox, QWidget

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


class QLabelFMR(QLabel):

    def __init__(self):
        super().__init__()

    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        print("pos1: ", ev.pos())

    def mouseReleaseEvent(self, ev: QtGui.QMouseEvent) -> None:
        print("pos3: ", ev.pos())


class EditorWidget(QDialog):

    def __init__(self, filepath, ui):
        super().__init__()

        self.ui_parent = ui
        self.filepath = filepath
        self.layout = QVBoxLayout()
        self.load_widgets(ui)
        self.setLayout(self.layout)
        self.set_image()

    def set_image(self):
        self.image = ImageFMR(self.filepath)
        self.image_label.setPixmap(self.image.to_pixmap())

    def load_widgets(self, ui):
        self.image_label = QLabelFMR()
        self.layout.addWidget(self.image_label)

        buttons_widget = QWidget()
        buttons_layout = QHBoxLayout()
        buttons_widget.setLayout(buttons_layout)

        validate = QPushButton("Validate")
        cancel = QPushButton("Cancel")

        buttons_layout.addWidget(validate)
        buttons_layout.addWidget(cancel)

        validate.clicked.connect(self.confirm)
        cancel.clicked.connect(self.cancel)

        self.layout.addWidget(buttons_widget)

    def cancel(self):
        self.ui_parent.confirmEvent.emit(False)

    def confirm(self):
        self.ui_parent.confirmEvent.emit(True)

from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel

from src.model.image_fmr import ImageFMR


class QLabelFMR(QLabel):

    def __init__(self):
        super().__init__()

    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        print("pos1: ", ev.pos())

    def mouseReleaseEvent(self, ev: QtGui.QMouseEvent) -> None:
        print("pos3: ", ev.pos())


class EditorWidget(QWidget):
    layout: QHBoxLayout
    image: ImageFMR
    image_label: QLabel

    def __init__(self):
        super().__init__()

        self.layout = QHBoxLayout()
        self.image_label = QLabelFMR()
        self.layout.addWidget(self.image_label)
        self.setLayout(self.layout)
        self.show()

    def set_image(self, filepath):
        self.image = ImageFMR(filepath)
        self.image_label.setPixmap(self.image.to_pixmap())

from PyQt5 import QtGui
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QDialog, QInputDialog, QPushButton, QVBoxLayout

from src.controller.action.editor_window import on_click_validate
from src.model.image_fmr import ImageFMR


class QLabelFMR(QLabel):

    def __init__(self):
        super().__init__()

    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        print("pos1: ", ev.pos())

    def mouseReleaseEvent(self, ev: QtGui.QMouseEvent) -> None:
        print("pos3: ", ev.pos())


class EditorWidget(QDialog):
    layout: QVBoxLayout
    image: ImageFMR
    image_label: QLabel

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.load_widgets()
        self.setLayout(self.layout)

    def set_image(self, filepath):
        self.image = ImageFMR(filepath)
        self.image_label.setPixmap(self.image.to_pixmap())

    def load_widgets(self):
        self.image_label = QLabelFMR()
        self.layout.addWidget(self.image_label)

        validate = QPushButton("Valider")
        validate.clicked.connect(lambda: on_click_validate(self))
        self.layout.addWidget(validate)



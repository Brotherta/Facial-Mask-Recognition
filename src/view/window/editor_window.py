import PIL
from PIL.ImageQt import ImageQt
from PyQt5 import QtGui, QtCore, Qt
from PyQt5.QtCore import QPoint, QRect
from PyQt5.QtGui import QPixmap, QIcon, QPainter, QColor, QFont
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QDialog, QInputDialog, QPushButton, QVBoxLayout, QMessageBox, QWidget

MAX_IMAGE_SIZE = (1600, 900)


class ImageFMR:
    filepath: str

    def __init__(self, filepath: str):
        self.filepath = filepath

    def to_pixmap(self) -> QPixmap:
        image = PIL.Image.open(self.filepath).convert("RGBA")
        self.resize_image(image)
        return QPixmap.fromImage(ImageQt(image))

    def to_icon(self) -> QIcon:
        return QIcon(self.filepath)

    def resize_image(self, image):
        if image.width > 1600 or image.height > 900:
            image.thumbnail(MAX_IMAGE_SIZE)

    def save_image(self, folderpath):
        pass


class QLabelFMR(QLabel):

    def __init__(self):
        self.previousMousePosition: QPoint = None
        super().__init__()

    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        print("pos1: ", ev.pos())
        self.previousMousePosition = ev.pos()

    def mouseReleaseEvent(self, ev: QtGui.QMouseEvent) -> None:

        x = min(self.previousMousePosition.x(), ev.pos().x())
        y = min(self.previousMousePosition.y(), ev.pos().y())
        width = max(self.previousMousePosition.x(), ev.pos().x()) - x
        height = max(self.previousMousePosition.y(), ev.pos().y()) - y
        print(x, y, width, height)
        new_pixmap = self.pixmap().copy()
        painter = QPainter(new_pixmap)
        painter.setPen(QColor("white"))
        rect = QRect(x, y, width, height)
        painter.fillRect(rect, QColor(255, 255, 255, 50))
        painter.end()
        self.setPixmap(new_pixmap.copy())
        self.previousMousePosition = None


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

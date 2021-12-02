import PIL
from PIL.ImageQt import ImageQt
from PyQt5 import QtGui, QtCore, Qt
from PyQt5.QtCore import QPoint, QRect
from PyQt5.QtGui import QPixmap, QIcon, QPainter, QColor, QFont
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QDialog, QInputDialog, QPushButton, QVBoxLayout, QMessageBox, QWidget

from src.model.image_fmr import ImageFMR


class EditorWidget(QDialog):
    draw_rect_event = QtCore.pyqtSignal(QRect)

    def __init__(self, image: ImageFMR, ui):
        super().__init__()

        self.draw_rect_event.connect(self.draw_rect)
        self.ui_parent = ui
        self.image = image
        self.layout = QVBoxLayout()
        self.load_widgets(ui)
        self.setLayout(self.layout)

    def load_widgets(self, ui):
        self.image_label = QLabelFMR(self.image, self.draw_rect_event)
        for rect in self.image.rects:
            self.draw_rect(rect)

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

    def draw_rect(self, rect: QRect):
        new_pixmap = self.image_label.pixmap().copy()
        painter = QPainter(new_pixmap)
        painter.fillRect(rect, QColor(171, 71, 188, 120))
        painter.end()
        self.image_label.setPixmap(new_pixmap)


class QLabelFMR(QLabel):

    def __init__(self, image: ImageFMR, draw_rect_signal):
        self.previousMousePosition: QPoint = None
        super().__init__()
        self.draw_rect_signal = draw_rect_signal
        self.image = image
        self.setPixmap(image.to_pixmap())

    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        self.previousMousePosition = ev.pos()

    def mouseReleaseEvent(self, ev: QtGui.QMouseEvent) -> None:
        x = min(self.previousMousePosition.x(), ev.pos().x())
        y = min(self.previousMousePosition.y(), ev.pos().y())
        width = max(self.previousMousePosition.x(), ev.pos().x()) - x
        height = max(self.previousMousePosition.y(), ev.pos().y()) - y

        rect = QRect(x, y, width, height)

        self.image.add_rect(rect)
        self.draw_rect_signal.emit(rect)
        self.previousMousePosition = None

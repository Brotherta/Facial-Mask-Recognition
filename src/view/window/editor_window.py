import PIL
from PIL.ImageQt import ImageQt
from PyQt5 import QtGui, QtCore, Qt
from PyQt5.QtCore import QPoint, QRect
from PyQt5.QtGui import QPixmap, QIcon, QPainter, QColor, QFont
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QDialog, QInputDialog, QPushButton, QVBoxLayout, QMessageBox, QWidget, \
    QGraphicsView, QGraphicsScene, QGraphicsRectItem

from src.model.box import Box
from src.model.image_fmr import ImageFMR

MAX_IMAGE_SIZE = (1200, 675)


class EditorWidget(QDialog):
    draw_rect_event = QtCore.pyqtSignal(Box)

    def __init__(self, image: ImageFMR, ui):
        super().__init__()

        self.draw_rect_event.connect(self.draw_rect)
        self.ui_parent = ui
        self.image = image
        self.image_label: QLabelFMR

        self.layout = QVBoxLayout()
        self.load_widgets(ui)
        self.setLayout(self.layout)

    def load_widgets(self, ui):
        self.image_label = QLabelFMR(self.image, self.draw_rect_event, self.ui_parent.assign_label_box)
        for box in self.image.boxs:
            self.draw_rect(box)

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

    # def draw_rect(self, box: Box):
    #     new_pixmap = self.image_label.pixmap().copy()
    #     painter = QPainter(new_pixmap)
    #     painter.fillRect(box.rect, QColor(171, 71, 188, 120))
    #     painter.end()
    #     self.image_label.setPixmap(new_pixmap)


class QLabelFMR(QGraphicsView):

    def __init__(self, image: ImageFMR, draw_rect_signal, assign_label_box):
        self.previousMousePosition: QPoint = None
        super().__init__()
        self.draw_rect_signal = draw_rect_signal
        self.assign_label_box = assign_label_box
        self.image = image
        self.scene = QGraphicsScene()

        self.scene.addPixmap(image.to_pixmap())
        self.r = QGraphicsRectItem()
        self.r
        self.setScene(self.scene)

    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        print(ev.pos())
        # if ev.button() == QtCore.Qt.LeftButton:
        #     self.previousMousePosition = ev.pos()
        # elif ev.button() == QtCore.Qt.RightButton:
        #     for box in self.image.boxs:
        #         if box.rect.contains(ev.pos()):
        #             self.assign_label_box.emit(box)
        #             break

    def drawRect(self, QPoint):


    # def mouseReleaseEvent(self, ev: QtGui.QMouseEvent) -> None:
    #     if self.previousMousePosition is not None and ev.button() == QtCore.Qt.LeftButton:
    #         x = min(self.previousMousePosition.x(), ev.pos().x())
    #         y = min(self.previousMousePosition.y(), ev.pos().y())
    #         width = max(self.previousMousePosition.x(), ev.pos().x()) - x
    #         height = max(self.previousMousePosition.y(), ev.pos().y()) - y
    #         self.previousMousePosition = None
    #
    #         box = Box(QRect(x, y, width, height), None)
    #
    #         self.image.add_box(box)
    #         self.assign_label_box.emit(box)
    #         self.draw_rect_signal.emit(box)





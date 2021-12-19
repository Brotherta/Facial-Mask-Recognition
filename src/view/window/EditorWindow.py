from PyQt5 import QtGui
from PyQt5.QtCore import QPoint
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QHBoxLayout, QDialog, QPushButton, QVBoxLayout, QWidget, \
    QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsSceneMouseEvent, QInputDialog, QAction, QMenu

from src.model.Box import Box
from src.model.ImageFMR import ImageFMR


class EditorWidget(QDialog):

    def __init__(self, image: ImageFMR, labels):
        super().__init__()
        self.imageLabel: QLabelFMR
        self.labels = labels
        self.validate = None
        self.cancel = None
        self.image = image
        self.adjustSize()
        self.layout = QVBoxLayout()
        self.loadWidgets()
        self.setLayout(self.layout)
        self.setWindowTitle("Editor")
        self.setWindowIcon(QIcon("assets/icon.png"))

    def loadWidgets(self):
        self.imageLabel = QLabelFMR(self.image, self.labels)
        self.layout.addWidget(self.imageLabel)

        buttonsWidget = QWidget()
        buttonsLayout = QHBoxLayout()
        buttonsWidget.setLayout(buttonsLayout)

        self.validate = QPushButton("Validate", self)
        self.cancel = QPushButton("Cancel", self)

        buttonsLayout.addWidget(self.validate)
        buttonsLayout.addWidget(self.cancel)

        self.layout.addWidget(buttonsWidget)


class QLabelFMR(QGraphicsView):

    def __init__(self, image: ImageFMR, labels):
        super().__init__()

        self.previousMousePosition = None
        self.firstPosition = None
        self.currentRect = None
        self.image = image
        self.labels = labels
        self.boxListTemp = []

        self.imagePixmap = image.toPixmap()
        self.scene = QGraphicsScene(0, 0, self.imagePixmap.width() - 10, self.imagePixmap.height() - 10)
        self.setMaximumSize(self.imagePixmap.width(), self.imagePixmap.height())
        self.adjustSize()

        self.scene.addPixmap(self.imagePixmap)
        self.loadBox()
        self.setScene(self.scene)

    def contextMenuEvent(self, event: QtGui.QContextMenuEvent) -> None:
        menu = QMenu(self)
        self.deleteBoxAction = QAction("Delete a box", self)
        self.deleteBoxAction.triggered.connect(lambda: self.deleteBox(event.pos()))
        menu.addAction(self.deleteBoxAction)
        action = menu.exec_(self.mapToGlobal(event.pos()))

    def deleteBox(self, pos: QPoint):
        result = self.getBoxAtPos(pos)
        if result is not None:
            self.boxListTemp.remove(result)
            self.scene.removeItem(result)

    def loadBox(self):
        for box in self.image.boxList:
            self.boxListTemp.append(box)
            box: Box
            if box.label is None:
                box.setBrush(Qt.white)
            else:
                box.setBrush(Qt.darkGreen)
            box.setOpacity(0.4)
            self.scene.addItem(box)

    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        if ev.button() == Qt.LeftButton:
            pos = ev.pos() + QPoint(self.horizontalScrollBar().value(), self.verticalScrollBar().value())
            self.firstPosition = pos

    def mouseMoveEvent(self, ev: QtGui.QMouseEvent) -> None:
        pos = ev.pos() + QPoint(self.horizontalScrollBar().value(), self.verticalScrollBar().value())
        if pos != self.firstPosition:
            if self.currentRect is not None:
                self.scene.removeItem(self.currentRect)

            self.drawRect(self.firstPosition, pos)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            if self.currentRect is not None:
                x = self.currentRect.rect().x()
                y = self.currentRect.rect().y()
                width = self.currentRect.rect().width()
                height = self.currentRect.rect().height()

                if width > 5 and height > 5 and width * height > 40:
                    self.boxListTemp.append(self.currentRect)
                else:
                    self.scene.removeItem(self.currentRect)

                self.currentRect = None
                self.firstPosition = None

    def drawRect(self, pos1: QPoint, pos2: QPoint):
        x = min(pos1.x(), pos2.x())
        y = min(pos1.y(), pos2.y())
        width = max(pos1.x(), pos2.x()) - x
        height = max(pos1.y(), pos2.y()) - y
        rec = Box(x, y, width, height)
        rec.setBrush(Qt.white)
        rec.setOpacity(0.4)
        self.scene.addItem(rec)
        self.currentRect = rec

    def mouseDoubleClickEvent(self, event: QtGui.QMouseEvent) -> None:
        items = list(map(lambda x: x.name, self.labels))
        items.append("None")
        if len(items) > 0:
            pos = event.pos() + QPoint(self.horizontalScrollBar().value(), self.verticalScrollBar().value())
            box = self.getBoxAtPos(pos)
            if box is not None:
                text, ok = QInputDialog.getItem(self,
                                                "Choose a label", "Labels : ",
                                                items)
                if ok and text:
                    if text == "None":
                        box.label = None
                        box.setBrush(Qt.white)
                    else:
                        for label in self.labels:
                            if label.name == text:
                                box.label = label
                                box.setBrush(Qt.darkGreen)
                                break

    def getBoxAtPos(self, pos: QPoint) -> Box:
        retBox = None
        for box in self.boxListTemp:
            x = box.x
            y = box.y
            w = box.width
            h = box.height
            if x <= pos.x() <= x + w and y <= pos.y() <= y + h:
                retBox = box

        return retBox

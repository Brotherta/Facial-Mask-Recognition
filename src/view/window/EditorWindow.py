from typing import Union

from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QPoint, pyqtSignal
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QHBoxLayout, QDialog, QPushButton, QVBoxLayout, QWidget, \
    QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsSceneMouseEvent, QInputDialog, QAction, QMenu, QComboBox

from src.data.DataContainer import DataContainer
from src.model.Box import Box
from src.model.ImageFMR import ImageFMR
from src.model.Label import Label
from utils.utils import Intersection


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
    clickOnBox = QtCore.pyqtSignal(Box)

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

        self.setAlignment(Qt.AlignCenter)
        self.scene.addPixmap(self.imagePixmap)
        self.loadBox()
        self.setScene(self.scene)

    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        if ev.button() == Qt.LeftButton:
            pos = ev.pos() + QPoint(self.horizontalScrollBar().value(), self.verticalScrollBar().value())
            self.firstPosition = pos

    def mouseMoveEvent(self, ev: QtGui.QMouseEvent) -> None:
        if self.firstPosition is not None:
            pos = ev.pos() + QPoint(self.horizontalScrollBar().value(), self.verticalScrollBar().value())
            if pos != self.firstPosition:
                if (self.image.imageSize[0] >= ev.x() >= 0
                        and self.image.imageSize[1] >= ev.y() >= 0):
                    if self.currentRect is not None:
                        self.scene.removeItem(self.currentRect)
                    self.drawRect(self.firstPosition, pos)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        self.currentRect: Box
        if event.button() == Qt.LeftButton:
            if self.currentRect is not None:
                x = self.currentRect.rect().x()
                y = self.currentRect.rect().y()
                width = self.currentRect.rect().width()
                height = self.currentRect.rect().height()

                if width > 5 and height > 5 and width * height > 40:
                    self.boxListTemp.append(self.currentRect)
                    self.verifyOthers(self.currentRect)
                else:
                    self.scene.removeItem(self.currentRect)
                    if self.currentRect in self.boxListTemp:
                        self.boxListTemp.remove(self.currentRect)

                self.currentRect = None
                self.firstPosition = None

    def mouseDoubleClickEvent(self, event: QtGui.QMouseEvent) -> None:
        items = list(map(lambda x: x.name, self.labels))
        items.append("None")
        if len(items) > 0:
            pos = event.pos() + QPoint(self.horizontalScrollBar().value(), self.verticalScrollBar().value())
            box = self.getBoxAtPos(pos)
            if box is not None:
                self.clickOnBox.emit(box)
                # dialog = LabelDoubleClickDialog(box, self, self.labels)
                # dialog.exec()

    def contextMenuEvent(self, event: QtGui.QContextMenuEvent) -> None:
        menu = QMenu(self)
        self.deleteBoxAction = QAction("Delete a box", self)
        self.deleteBoxAction.triggered.connect(lambda: self.deleteBox(event.pos()))
        menu.addAction(self.deleteBoxAction)
        action = menu.exec_(self.mapToGlobal(event.pos()))

    def deleteBox(self, pos: QPoint):
        pos = pos + QPoint(self.horizontalScrollBar().value(), self.verticalScrollBar().value())
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

    def drawRect(self, pos1: QPoint, pos2: QPoint):
        x = min(pos1.x(), pos2.x())
        y = min(pos1.y(), pos2.y())
        width = max(pos1.x(), pos2.x()) - x
        height = max(pos1.y(), pos2.y()) - y
        rec = Box(x, y, width, height)
        rec.setBrush(Qt.white)
        rec.setOpacity(0.4)
        self.scene.addItem(rec)
        self.currentRect: Box = rec

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

    def verifyOthers(self, rect: Box):
        UL = QPoint(rect.x, rect.y)  # Up Left
        UR = QPoint(rect.x + rect.width, rect.y)  # Up Right
        DL = QPoint(rect.x, rect.y + rect.height)  # Down Left
        DR = QPoint(rect.x + rect.width, rect.y + rect.height)  # Down Right
        originRectArea = Intersection.getArea(UL, UR, DL)

        boxToRemove = []
        for r in self.boxListTemp:
            r: Box
            UL_R = QPoint(r.x, r.y)
            UR_R = QPoint(r.x + r.width, r.y)
            DL_R = QPoint(r.x, r.y + r.height)
            DR_R = QPoint(r.x + r.width, r.y + r.height)
            rectArea = Intersection.getArea(UL_R, UR_R, DL_R)

            UL_C: QPoint
            UR_C: QPoint
            DL_C: QPoint
            DR_C: QPoint

            # UL_C
            if Intersection.isInRect(UL, r):
                UL_C = UL
            elif Intersection.isInRect(UL_R, rect):
                UL_C = UL_R
            else:
                UL_C_1 = Intersection.isIntersection(UL, DL, UL_R, UR_R)
                UL_C_2 = Intersection.isIntersection(UL_R, DL_R, UL, UR)

                if UL_C_1 is not None:
                    UL_C = UL_C_1
                elif UL_C_2 is not None:
                    UL_C = UL_C_2
                else:  # no intersection
                    continue

            # UR_C
            if Intersection.isInRect(UR, r):
                UR_C = UR
            elif Intersection.isInRect(UR_R, rect):
                UR_C = UR_R
            else:
                UR_C_1 = Intersection.isIntersection(UR, DR, UL_R, UR_R)
                UR_C_2 = Intersection.isIntersection(UR_R, DR_R, UL, UR)

                if UR_C_1 is not None:
                    UR_C = UR_C_1
                elif UR_C_2 is not None:
                    UR_C = UR_C_2
                else:  # no intersection
                    continue

            # DL_C
            if Intersection.isInRect(DL, r):
                DL_C = DL
            elif Intersection.isInRect(DL_R, rect):
                DL_C = DL_R
            else:
                DL_C_1 = Intersection.isIntersection(UL, DL, DL_R, DR_R)
                DL_C_2 = Intersection.isIntersection(UL_R, DL_R, DL, DR)

                if DL_C_1 is not None:
                    DL_C = DL_C_1
                elif DL_C_2 is not None:
                    DL_C = DL_C_2
                else:  # no intersection
                    continue

            # DR_C
            if Intersection.isInRect(DR, r):
                DR_C = DR
            elif Intersection.isInRect(DR_R, rect):
                DR_C = DR_R
            else:
                DR_C_1 = Intersection.isIntersection(UR, DR, DL_R, DR_R)
                DR_C_2 = Intersection.isIntersection(UR_R, DR_R, DL, DR)

                if DR_C_1 is not None:
                    DR_C = DR_C_1
                elif DR_C_2 is not None:
                    DR_C = DR_C_2
                else:  # no intersection
                    continue

            collisionArea = Intersection.getArea(UL_C, UR_C, DL_C)
            if (rectArea/100 * 20) < collisionArea:
                boxToRemove.append(r)
                # self.scene.remov
            elif (originRectArea/100*20) < collisionArea:
                boxToRemove.append(rect)
                # self.s
                break

        for r in boxToRemove:
            self.scene.removeItem(r)
            self.boxListTemp.remove(r)
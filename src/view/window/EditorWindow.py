from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QPoint
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QHBoxLayout, QDialog, QPushButton, QVBoxLayout, QWidget, \
    QGraphicsView, QGraphicsScene, QAction, QMenu

from src.model.Box import Box
from src.model.ImageFMR import ImageFMR
from utils.utils import Intersection


# The image editor window, which allow to draw box, assign labels... on images.
class EditorWidget(QDialog):

    def __init__(self, image: ImageFMR, labels):
        super().__init__()
        self.imageLabel: QLabelFMR  # Contain the image displayed
        self.labels = labels  # Contain the project labels
        self.validate = None
        self.cancel = None
        self.image = image  # Contain the Image Object

        self.adjustSize()
        self.layout = QVBoxLayout()  # Vertical layout
        self.loadWidgets()

        self.setLayout(self.layout)
        self.setWindowTitle("Editor")
        self.setWindowIcon(QIcon("assets/icon.png"))

    def loadWidgets(self):
        """ Load the window widgets. """
        self.imageLabel = QLabelFMR(self.image, self.labels)  # Load or custom image container
        self.layout.addWidget(self.imageLabel)

        # Buttons widgets/layout
        buttonsWidget = QWidget()  # Contains the button at the bottom of the window, to valide or cancel changes
        buttonsLayout = QHBoxLayout()  # Horizontal layouts for the buttons
        buttonsWidget.setLayout(buttonsLayout)

        # Buttons
        self.validate = QPushButton("Validate", self)
        self.cancel = QPushButton("Cancel", self)
        buttonsLayout.addWidget(self.validate)
        buttonsLayout.addWidget(self.cancel)

        self.layout.addWidget(buttonsWidget)


# Our custom QGraphicsView. Will contain the image, and make the manipulations more easier.
class QLabelFMR(QGraphicsView):
    clickOnBox = QtCore.pyqtSignal(Box)

    def __init__(self, image: ImageFMR, labels):
        super().__init__()

        # Temporary values, used for boxes drawing (see later)
        self.previousMousePosition = None
        self.firstPosition = None # The position of the first mouse left button click, root of the rectangle
        self.currentRect = None  # The rectangle drawn by the mouse

        self.image = image  # The image object
        self.imagePixmap = image.toPixmap()  # Load the pixmap from the image object
        self.labels = labels  # The project labels
        self.boxListTemp = []  # The actual list of boxes

        # Create the scene
        self.scene = QGraphicsScene(0, 0, self.imagePixmap.width() - 10, self.imagePixmap.height() - 10)
        self.setMaximumSize(self.imagePixmap.width(), self.imagePixmap.height())
        self.adjustSize()

        self.setAlignment(Qt.AlignCenter)
        self.scene.addPixmap(self.imagePixmap)  # Adding the image to the scene
        self.loadBoxes()  # Loading the boxes already defined before (save) and display them
        self.setScene(self.scene)

    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        """ Catching the mouse left button click. """
        if ev.button() == Qt.LeftButton:
            pos = ev.pos() + QPoint(self.horizontalScrollBar().value(), self.verticalScrollBar().value())
            self.firstPosition = pos  # Now we know that we already began a left click, at this position

    def mouseMoveEvent(self, ev: QtGui.QMouseEvent) -> None:
        """ If the mouse move while holding left mouse button (first position not null). """
        if self.firstPosition is not None:
            pos = ev.pos() + QPoint(self.horizontalScrollBar().value(), self.verticalScrollBar().value())

            # Draw a rectangle following the mouse
            if pos != self.firstPosition:

                if (self.image.imageSize[0] >= ev.x() >= 0
                        and self.image.imageSize[1] >= ev.y() >= 0):
                    # If a rectangle is already drawn, delete it
                    if self.currentRect is not None:
                        self.scene.removeItem(self.currentRect)

                    self.drawRect(self.firstPosition, pos)  # Draw the rectangle

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        """ Catching the mouse left button release event. """
        self.currentRect: Box
        if event.button() == Qt.LeftButton:
            if self.currentRect is not None:  # If a rectangle has been drawn
                width = self.currentRect.rect().width()
                height = self.currentRect.rect().height()

                # If the rectangle dimension are correct
                if width > 5 and height > 5 and width * height > 40:
                    self.boxListTemp.append(self.currentRect)
                    self.verifyOthers(self.currentRect)
                # Else we delete it
                else:
                    self.scene.removeItem(self.currentRect)  # Remove from the scene
                    if self.currentRect in self.boxListTemp:  # Remove from our rect list
                        self.boxListTemp.remove(self.currentRect)

                # Reset temporary values
                self.currentRect = None
                self.firstPosition = None

    def mouseDoubleClickEvent(self, event: QtGui.QMouseEvent) -> None:
        """ Catching mouse double click, displaying the box properties. """
        items = list(map(lambda x: x.name, self.labels))  # A list of all project labels names
        items.append("None")

        # Getting which box is double clicked
        pos = event.pos() + QPoint(self.horizontalScrollBar().value(), self.verticalScrollBar().value())
        box = self.getBoxAtPos(pos)
        if box is not None:
            self.clickOnBox.emit(box)  # Emit the signal to the controller which will launch the dialog

    def contextMenuEvent(self, event: QtGui.QContextMenuEvent) -> None:
        """ When the contextual menu need to be displayed. """
        menu = QMenu(self)

        # Delete box action
        self.deleteBoxAction = QAction("Delete a box", self)
        self.deleteBoxAction.triggered.connect(lambda: self.deleteBox(event.pos()))
        menu.addAction(self.deleteBoxAction)

        menu.exec_(self.mapToGlobal(event.pos()))  # Showing the contextual menu

    def deleteBox(self, pos: QPoint):
        """ Given a position, delete the box associated. """
        pos = pos + QPoint(self.horizontalScrollBar().value(), self.verticalScrollBar().value())
        result = self.getBoxAtPos(pos)  # Getting the box which is at this position

        # Delete it
        if result is not None:
            self.boxListTemp.remove(result)
            self.scene.removeItem(result)

    def loadBoxes(self):
        """ Load and display boxes already defined on this image. """
        for i in range(len(self.image.boxList)):
            box = self.image.boxList[i]
            self.image.boxList[i] = Box(box.x, box.y, box.width, box.height)
            self.image.boxList[i].label = box.label
            box = self.image.boxList[i]
            self.boxListTemp.append(box)  # Adding the box to our list
            box: Box
            
            if box.label is None:  # If a label has already been assigned, then white rectangle
                box.setBrush(Qt.white)
            else:
                box.setBrush(Qt.darkGreen)  # Not assigned box has dark green color
            box.setOpacity(0.4)
            self.scene.addItem(box)  # Adding the box to the scene

    def drawRect(self, pos1: QPoint, pos2: QPoint):
        """ Draw a rectangle into the scene. """
        x = min(pos1.x(), pos2.x())
        y = min(pos1.y(), pos2.y())
        width = max(pos1.x(), pos2.x()) - x
        height = max(pos1.y(), pos2.y()) - y

        # create a white transparent box
        rec = Box(x, y, width, height)
        rec.setBrush(Qt.white)
        rec.setOpacity(0.4)

        # Adding to the scene
        self.scene.addItem(rec)
        self.currentRect: Box = rec

    def getBoxAtPos(self, pos: QPoint) -> Box:
        """ Given a position, return the box associated. """
        retBox = None  # The box
        for box in self.boxListTemp:
            x = box.x
            y = box.y
            w = box.width
            h = box.height

            # If the given position is on this box
            if x <= pos.x() <= x + w and y <= pos.y() <= y + h:
                retBox = box # Assign the box

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
            if (rectArea / 100 * 20) < collisionArea:
                boxToRemove.append(r)
                # self.scene.remov
            elif (originRectArea / 100 * 20) < collisionArea:
                boxToRemove.append(rect)
                # self.s
                break

        for r in boxToRemove:
            self.scene.removeItem(r)
            self.boxListTemp.remove(r)

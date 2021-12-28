from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QListWidget, QSizePolicy, QListWidgetItem, QAbstractItemView, QAction

from src.model.ImageFMR import ImageFMR


# The widget display the list of the images loaded into the project
class ImagesListWidget(QListWidget):
    delKeyPressSignal = QtCore.pyqtSignal()  # This signal is connected to the main controller

    def __init__(self):
        super().__init__()

        # Widget
        self.editorWindow = None
        self.setViewMode(QListWidget.ViewMode.IconMode)
        self.setResizeMode(QListWidget.ResizeMode.Adjust)
        self.setAcceptDrops(False)
        self.setIconSize(QSize(200, 133))
        self.setSpacing(20)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)

        # Size policy
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(3)
        self.setSizePolicy(sizePolicy)

        # Contextual menu. Allows use to delete image from right click
        self.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.deleteAction = QAction("Delete image", self)
        self.addAction(self.deleteAction)

    def addImage(self, image: ImageFMR):
        """ Add an image to the widget list. """
        imageWidgetItem = ImageWidgetItem(image, self)
        self.addItem(imageWidgetItem)

    def keyPressEvent(self, e: QtGui.QKeyEvent) -> None:
        """ Catch the delete button press event, and emit a signal to delete the image associated. """
        if e.key() == Qt.Key_Delete:
            self.delKeyPressSignal.emit()


# A custom list widget item which can be initialised from an Image Object
class ImageWidgetItem(QListWidgetItem):
    image: ImageFMR
    parent: ImagesListWidget

    def __init__(self, image: ImageFMR, parent):
        super().__init__()

        self.parent = parent
        self.image = image
        self.setIcon(QIcon(image.filepath))  # Load the image into the widget

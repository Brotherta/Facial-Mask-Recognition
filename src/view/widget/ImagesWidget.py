from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QListWidget, QSizePolicy, QListWidgetItem, QAbstractItemView, QAction

from src.model.ImageFMR import ImageFMR


class ImagesListWidget(QListWidget):
    delKeyPressSignal = QtCore.pyqtSignal()

    def __init__(self):
        super(ImagesListWidget, self).__init__()
        self.editorWindow = None
        self.setViewMode(QListWidget.ViewMode.IconMode)
        self.setResizeMode(QListWidget.ResizeMode.Adjust)
        self.setAcceptDrops(False)
        self.setIconSize(QSize(200, 133))
        self.setSpacing(20)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)

        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(3)
        self.setSizePolicy(sizePolicy)

        self.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.deleteAction = QAction("Delete image", self)
        self.addAction(self.deleteAction)

    def addImage(self, image: ImageFMR):
        imageWidgetItem = ImageWidgetItem(image, self)
        self.addItem(imageWidgetItem)

    def keyPressEvent(self, e: QtGui.QKeyEvent) -> None:
        if e.key() == Qt.Key_Delete:
            self.delKeyPressSignal.emit()


class ImageWidgetItem(QListWidgetItem):
    image: ImageFMR
    parent: ImagesListWidget

    def __init__(self, image: ImageFMR, parent):
        QListWidgetItem.__init__(self)
        self.parent = parent
        self.image = image
        self.setIcon(QIcon(image.filepath))

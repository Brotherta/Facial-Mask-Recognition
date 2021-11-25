from PyQt5 import QtGui
from common import *
from src.controller.menu import *


class ListImageWidget(QListWidget):

    def __init__(self):
        QListWidget.__init__(self)

        self.setViewMode(QListWidget.ViewMode.IconMode)
        self.setResizeMode(QListWidget.ResizeMode.Adjust)
        self.setAcceptDrops(True)
        self.setIconSize(QSize(200, 133))
        # self.setItemAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.setContentsMargins(QMargins(0, 30, 0, 30))
        self.setSpacing(20)
        
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(3)
        self.setSizePolicy(sizePolicy)


    def mouseDoubleClickEvent(self, e: QtGui.QMouseEvent) -> None:
        print("double click !")


    def add_image(self, filepath):
        listWidgetItem = QListWidgetItem()
        listWidgetItem.setIcon(QIcon(filepath))
        self.addItem(listWidgetItem)
        
        
        
    
        
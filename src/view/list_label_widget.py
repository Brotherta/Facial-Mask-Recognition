from PyQt5 import QtGui
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QListWidget, QSizePolicy, QWidget


class ListLabelsWidget(QListWidget):

    def __init__(self):
        QListWidget.__init__(self)
        self.setMaximumWidth(150)
        self.setStyleSheet("QListWidget { border: 1px solid red }")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        self.setSizePolicy(sizePolicy)
    
    def mouseDoubleClickEvent(self, e: QtGui.QMouseEvent) -> None:
        print("double click !")
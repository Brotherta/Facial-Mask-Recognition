from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QListWidget, QSizePolicy, QPushButton, QListWidgetItem

import utils.utils
from src import *


class LabelsListWidget(QListWidget):
    delEvent = QtCore.pyqtSignal()

    def __init__(self):
        super(LabelsListWidget, self).__init__()

        self.setMaximumWidth(200)
        self.setSpacing(10)
        self.setStyleSheet(utils.utils.load_stylesheet('style/labels.css'))

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy(Qt.ScrollBarAlwaysOff))

        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(3)
        self.setSizePolicy(size_policy)

        self.delete_item_action = QAction("Delete", self)
        self.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.addAction(self.delete_item_action)

    def add_label(self, label_name):
        label_widget_item = LabelWidgetItem(label_name, self)
        self.addItem(label_widget_item)

    def keyPressEvent(self, e: QtGui.QKeyEvent) -> None:
        if e.key() == Qt.Key_Delete:
            self.delEvent.emit()


class LabelWidgetItem(QListWidgetItem):
    parent: LabelsListWidget

    def __init__(self, name, parent):
        super(LabelWidgetItem, self).__init__()
        self.parent = parent
        self.setText(name)
        self.setToolTip(name)
        self.setTextAlignment(Qt.AlignCenter)

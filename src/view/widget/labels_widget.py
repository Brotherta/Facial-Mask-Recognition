from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QListWidget, QSizePolicy, QPushButton, QListWidgetItem

import utils.utils
from src import *
from src.model.label import Label


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

        self.setContextMenuPolicy(Qt.ActionsContextMenu)

        self.delete_item_action = QAction("Delete", self)
        self.addAction(self.delete_item_action)
        self.rename_item_action = QAction("Rename", self)
        self.addAction(self.rename_item_action)

    def add_label(self, label: Label):
        label_widget_item = LabelWidgetItem(label, self)
        self.addItem(label_widget_item)

    def remove_label(self, item):
        self.takeItem(self.row(item))

    def keyPressEvent(self, e: QtGui.QKeyEvent) -> None:
        if e.key() == Qt.Key_Delete:
            self.delEvent.emit()


class LabelWidgetItem(QListWidgetItem):
    parent: LabelsListWidget

    def __init__(self, label: Label, parent):
        super(LabelWidgetItem, self).__init__()
        self.parent = parent
        self.label = label
        self.setText(self.label.name)
        self.setToolTip(self.label.name)
        self.setTextAlignment(Qt.AlignCenter)

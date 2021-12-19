from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QListWidget, QSizePolicy, QPushButton, QListWidgetItem, QAction, QAbstractItemView

import utils.utils
from src.data.DataContainer import DataContainer
from src.model.Label import Label


class LabelsListWidget(QListWidget):
    delSignal = QtCore.pyqtSignal()

    def __init__(self):
        super(LabelsListWidget, self).__init__()
        self.setMaximumWidth(200)
        self.setSpacing(10)
        self.setStyleSheet(utils.utils.load_stylesheet('style/labels.css'))
        self.setAcceptDrops(False)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy(Qt.ScrollBarAlwaysOff))

        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(3)
        self.setSizePolicy(sizePolicy)

        self.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.createItemAction = QAction("Create new label", self)
        self.deleteItemAction = QAction("Delete a label", self)
        self.renameItemAction = QAction("Rename a label", self)
        self.addActions([self.createItemAction, self.deleteItemAction, self.renameItemAction])

    def addLabel(self, label: Label):
        labelWidgetItem = LabelWidgetItem(label, self)
        self.addItem(labelWidgetItem)

    def removeLabel(self, item):
        self.takeItem(self.row(item))

    def keyPressEvent(self, e: QtGui.QKeyEvent) -> None:
        if e.key() == Qt.Key_Delete:
            self.delSignal.emit()


class LabelWidgetItem(QListWidgetItem):
    parent: LabelsListWidget

    def __init__(self, label: Label, parent):
        super(LabelWidgetItem, self).__init__()
        self.parent = parent
        self.label = label
        self.setText(self.label.name)
        self.setToolTip(self.label.name)
        self.setTextAlignment(Qt.AlignCenter)

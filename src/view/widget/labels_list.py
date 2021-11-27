from PyQt5 import QtGui
from PyQt5.QtWidgets import QListWidget, QSizePolicy, QPushButton, QListWidgetItem

import utils.utils
from src import *


class LabelsListWidget(QListWidget):

    def __init__(self, annotator):
        self.annotator = annotator
        QListWidget.__init__(self)
        self.setMaximumWidth(200)
        self.setSpacing(10)
        self.setStyleSheet(utils.utils.load_stylesheet('style/labels.css'))

        self.itemDoubleClicked.connect(self.annotator.rename_label)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy(Qt.ScrollBarAlwaysOff))

        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(3)
        self.setSizePolicy(size_policy)

        act_item = QAction("Delete", self)
        act_item.triggered.connect(lambda: self.annotator.del_label(self.currentItem()))
        self.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.addAction(act_item)

    def add_label(self, label_name):
        label_widget_item = LabelWidgetItem(label_name, self)
        self.addItem(label_widget_item)

    def keyPressEvent(self, e: QtGui.QKeyEvent) -> None:
        if e.key() == Qt.Key_Delete:
            self.annotator.del_label(self.currentItem())


class LabelWidgetItem(QListWidgetItem):
    parent: LabelsListWidget

    def __init__(self, name, parent):
        QListWidgetItem.__init__(self)
        self.parent = parent
        self.setText(name)
        self.setToolTip(name)
        self.setTextAlignment(Qt.AlignCenter)


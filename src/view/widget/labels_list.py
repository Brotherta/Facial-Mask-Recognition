from PyQt5.QtWidgets import QListWidget, QSizePolicy, QPushButton, QListWidgetItem

import utils.utils
from src.controller.action.menu import import_label
from src import *


class LabelsListWidget(QListWidget):

    def __init__(self):
        QListWidget.__init__(self)
        self.setMaximumWidth(200)
        self.setSpacing(15)
        self.itemClicked.connect(import_label)
        self.setStyleSheet(utils.utils.load_stylesheet('style/labels.css'))

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy(Qt.ScrollBarAlwaysOff))

        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(1)
        self.setSizePolicy(size_policy)

    def add_label(self, label_name):
        label_widget_item = LabelWidgetItem(label_name, self)
        self.addItem(label_widget_item)


class LabelWidgetItem(QListWidgetItem):
    parent: LabelsListWidget

    def __init__(self, name, parent):
        QListWidgetItem.__init__(self)
        self.parent = parent
        self.setText(name)
        self.setToolTip(name)
        self.setTextAlignment(Qt.AlignCenter)

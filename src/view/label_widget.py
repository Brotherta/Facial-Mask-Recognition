from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QListWidget


class LabelsWidget(QListWidget):

    def __init__(self):
        QListWidget.__init__(self)
        self.setMaximumWidth(150)
        self.setStyleSheet("QListWidget { border: 1px solid red }")
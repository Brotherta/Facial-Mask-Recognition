from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QComboBox

from src.model.Box import Box


class LabelDoubleClickDialog(QDialog):

    def __init__(self, box: Box, labels):
        super().__init__()
        layout = QVBoxLayout()
        self.box = box
        self.labels = [] + labels
        self.setWindowTitle("Label")
        self.setWindowIcon(QIcon("assets/icon.png"))

        self.buttonDelete = QPushButton("Delete box")
        self.buttonOk = QPushButton("Validate")

        self.cb = QComboBox()
        items = list(map(lambda x: x.name, self.labels))
        self.cb.addItems(items)
        if self.box is not None and self.box.label is not None:
            if self.box.label.name is not None or self.box.label.name != "None":
                self.cb.setCurrentText(self.box.label.name)

        layout.addWidget(self.cb)
        layout.addWidget(self.buttonOk)
        layout.addWidget(self.buttonDelete)
        self.setLayout(layout)
        self.setMinimumWidth(200)



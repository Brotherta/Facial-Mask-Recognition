from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QComboBox

from src.model.Box import Box


# This dialog is show when a box is double clicked.
# It allow to redefine the label associated, and to delete it, and show the current label.
class LabelDoubleClickDialog(QDialog):

    def __init__(self, box: Box, labels):
        super().__init__()
        layout = QVBoxLayout()  # Vertical layout
        self.box = box  # The box which is double clicked
        self.labels = [] + labels  # The project labels

        self.setWindowTitle("Label")
        self.setWindowIcon(QIcon("assets/icon.png"))
        self.setMinimumWidth(200)

        # Buttons
        self.buttonDelete = QPushButton("Delete box")
        self.buttonOk = QPushButton("Validate")

        # The labels list
        self.cb = QComboBox()
        items = list(map(lambda x: x.name, self.labels))  # Getting the list of all labels name
        self.cb.addItems(items)  # Add the names to the list

        # Setting the list to display the current label associated, if there is one.
        if self.box is not None and self.box.label is not None:
            if self.box.label.name is not None or self.box.label.name != "None":
                self.cb.setCurrentText(self.box.label.name)

        # Layout
        layout.addWidget(self.cb)
        layout.addWidget(self.buttonOk)
        layout.addWidget(self.buttonDelete)
        self.setLayout(layout)




from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QListWidget, QSizePolicy, QListWidgetItem, QAction

import utils.utils
from src.model.Label import Label


# This widget contains the list of the project labels
class LabelsListWidget(QListWidget):
    delSignal = QtCore.pyqtSignal()  # This signal is connected to the main controller

    def __init__(self):
        super().__init__()

        # Widget
        self.setMaximumWidth(200)  # We want it on the left and not too big
        self.setSpacing(10)
        self.setStyleSheet(utils.utils.load_stylesheet('style/labels.css'))  # Custom CSS stylesheet
        self.setAcceptDrops(False)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy(Qt.ScrollBarAlwaysOff))

        # Size policy
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(3)
        self.setSizePolicy(sizePolicy)

        # Contextual menu, allow us to create delete and rename from right click.
        self.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.createItemAction = QAction("Create new label", self)
        self.deleteItemAction = QAction("Delete a label", self)
        self.renameItemAction = QAction("Rename a label", self)
        self.addActions([self.createItemAction, self.deleteItemAction, self.renameItemAction])

    def addLabel(self, label: Label):
        """ Add a label to the widget list. """
        labelWidgetItem = LabelWidgetItem(label, self)
        self.addItem(labelWidgetItem)

    def removeLabel(self, item):
        """ Remove a label from the widget list. """
        self.takeItem(self.row(item))

    def keyPressEvent(self, e: QtGui.QKeyEvent) -> None:
        """ Catch the delete key press event, and emit a signal to the controller to delete the label associated. """
        if e.key() == Qt.Key_Delete:
            self.delSignal.emit()


# A custom ListWidgetItem which can be initialised from a Label Object
class LabelWidgetItem(QListWidgetItem):
    parent: LabelsListWidget

    def __init__(self, label: Label, parent):
        super().__init__()
        self.parent = parent
        self.label = label

        # Assign the label name
        self.setText(self.label.name)
        self.setToolTip(self.label.name)

        self.setTextAlignment(Qt.AlignCenter)

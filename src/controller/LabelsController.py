from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QErrorMessage, QInputDialog, QMessageBox

from src.data.DataContainer import DataContainer
from src.model.Label import Label
from src.view.widget.LabelsWidget import LabelWidgetItem
from src.view.window.MainWindow import MainWindow


class LabelsController:

    def __init__(self, mainWindow: MainWindow, data: DataContainer):
        self.mainWindow = mainWindow
        self.data = data

    def setLabels(self):
        self.mainWindow.labelsWidget.clear()
        for label in self.data.labels:
            self.mainWindow.labelsWidget.addLabel(label)

    def searchForLabel(self, newName):
        for label in self.data.labels:
            if label.name == newName:
                error = QErrorMessage()
                error.showMessage(f"The label {newName} already exists !")
                error.exec_()
                return True
        return False

    def createLabel(self):
        dialog = QInputDialog(self.mainWindow)
        QInputDialog.setInputMode(dialog, QInputDialog.TextInput)
        dialog.resize(QSize(400, 200))
        dialog.setLabelText('Enter the name of the new label:')
        validate = dialog.exec_()
        name = dialog.textValue()

        if validate and not self.searchForLabel(name):
            newLabel = Label(name)
            self.data.labels.append(newLabel)
            self.mainWindow.labelsWidget.addLabel(newLabel)

    def renameLabel(self, item: LabelWidgetItem):
        dialog = QInputDialog(self.mainWindow)
        QInputDialog.setInputMode(dialog, QInputDialog.TextInput)
        dialog.resize(QSize(400, 200))
        dialog.setLabelText(f'Rename {item.text()} label for :')
        validate = dialog.exec_()
        newName = dialog.textValue()

        if validate and not self.searchForLabel(newName):
            for label in self.data.labels:
                if label.name == item.label.name:
                    label.name = newName
            item.setText(item.label.name)

    def deleteLabel(self, item):
        dialogue = QMessageBox(self.mainWindow)
        dialogue.setText(f"Delete {item.text()} label ?")
        dialogue.setWindowTitle("Delete labels")
        dialogue.addButton(QMessageBox.Yes)
        dialogue.addButton(QMessageBox.No)
        rep = dialogue.exec()
        if rep == QMessageBox.Yes:
            self.mainWindow.labelsWidget.removeLabel(item)
            for label in self.data.labels:
                if label == item.label:
                    self.data.labels.remove(label)
                    break

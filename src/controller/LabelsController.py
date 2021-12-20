import json
import os.path
import traceback
import pandas as pd

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QErrorMessage, QInputDialog, QMessageBox, QFileDialog, QComboBox

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
            item.setToolTip(item.label.name)

    def deleteLabel(self, items):
        for item in items:
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

    def importLabels(self):
        filepaths = QFileDialog.getOpenFileNames(parent=self.mainWindow, caption='Import categories',
                                                 filter="CSV, JSON (*.csv *json)")
        if len(filepaths[0]) > 0:
            for path in filepaths[0]:
                _, extension = os.path.splitext(path)
                if extension == ".json":
                    self.openJsonFile(path)
                elif extension == ".csv":
                    self.openCsvFile(path)

    def openJsonFile(self, path):
        labelList = []
        try:
            with open(path, 'r') as f:
                labels = json.load(f)
                f.flush()
                f.close()
        except json.JSONDecodeError as e:
            print(e)

        try:
            for label in labels:
                labelList.append(label['name'])
        except Exception as e:
            print(e, traceback.format_exc())

        self.addLabelsToWidget(labelList)

    def openCsvFile(self, path):
        labelList = []
        try:
            labels = pd.read_csv(path)
            columns = labels.columns
            if columns[0] == 'categories':
                labelList = labels['categories'].tolist()
                self.addLabelsToWidget(labelList)
            else:
                error = QErrorMessage()
                error.showMessage(f"the column name must me 'name' !")
                error.exec_()

        except Exception as e:
            print(e, traceback.format_exc())

    def addLabelsToWidget(self, labels):
        for labelName in labels:
            label = Label(labelName)
            if label not in self.data.labels:
                self.data.labels.append(label)
                self.mainWindow.labelsWidget.addLabel(label)

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


# This is the controller for the labels manipulations.
class LabelsController:

    def __init__(self, mainWindow: MainWindow, data: DataContainer):
        self.mainWindow = mainWindow
        self.data = data

    def setLabels(self):
        """ Add all labels of the data container into the labels widget. """
        self.mainWindow.labelsWidget.clear()
        for label in self.data.labels:
            self.mainWindow.labelsWidget.addLabel(label)

    def searchForLabel(self, newName):
        """ Return if the given name is a label already created. """
        for label in self.data.labels:
            if label.name == newName:
                error = QErrorMessage()  # Qt error dialog
                error.showMessage(f"The label {newName} already exists !")
                error.exec_()  # Show the error dialog to the user
                return True
        return False

    def createLabel(self):
        """ Open a dialog and prompt to the user which is the name of the new label. Imports it to the project. """
        # Open the dialog
        dialog = QInputDialog(self.mainWindow)
        QInputDialog.setInputMode(dialog, QInputDialog.TextInput)
        dialog.resize(QSize(400, 200))
        dialog.setLabelText('Enter the name of the new label:')
        validate = dialog.exec_()
        name = dialog.textValue()  # Getting the prompt text value

        # Add the new label to the data container and the widgets
        if validate and not self.searchForLabel(name):
            newLabel = Label(name)  # Create the label
            self.data.labels.append(newLabel)  # Data container
            self.mainWindow.labelsWidget.addLabel(newLabel)  # Widget

    def renameLabel(self, item: LabelWidgetItem):
        """ Set the value of an already created value. Prompt the new value in a dialog. """
        # Dialog
        dialog = QInputDialog(self.mainWindow)
        QInputDialog.setInputMode(dialog, QInputDialog.TextInput)
        dialog.resize(QSize(400, 200))
        dialog.setLabelText(f'Rename {item.text()} label for :')
        validate = dialog.exec_()
        newName = dialog.textValue()

        # If the user clicked validate and the new label value is not already created
        if validate and not self.searchForLabel(newName):
            for label in self.data.labels:
                if label.name == item.label.name:
                    label.name = newName
            item.setText(item.label.name)
            item.setToolTip(item.label.name)

    def deleteLabel(self, items):
        """ Delete a label from the widgets and the data container. Prompt the target in a dialog. """
        for item in items:
            # Dialog
            dialogue = QMessageBox(self.mainWindow)
            dialogue.setText(f"Delete {item.text()} label ?")
            dialogue.setWindowTitle("Delete labels")
            dialogue.addButton(QMessageBox.Yes)
            dialogue.addButton(QMessageBox.No)
            rep = dialogue.exec()

            # If the user really want to delete
            if rep == QMessageBox.Yes:
                self.mainWindow.labelsWidget.removeLabel(item)  # Remove from the widget
                for label in self.data.labels:
                    if label == item.label:
                        self.data.labels.remove(label)  # Remove from the data container
                        break

    def importLabels(self):
        """ Import existing labels from a json file with the file explorer. """
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
        """ Load existing labels from a json file and add them to the data container and the widget. """
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
        """ Load existing labels from a csv file and add them to the data container and the widget. Same as above. """
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
        """ Add the given labels list to the data container and the widget. """
        for labelName in labels:
            label = Label(labelName)
            if label not in self.data.labels:
                self.data.labels.append(label)
                self.mainWindow.labelsWidget.addLabel(label)

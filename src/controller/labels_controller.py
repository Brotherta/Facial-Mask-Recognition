from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QInputDialog, QMessageBox, QErrorMessage

from src.model.label import Label
from src.view.window.main_window import MainWindow


class LabelsController:

    def __init__(self, ui):
        self.main_ui: MainWindow = ui
        self.labels: list[Label] = []

    def name_already_existing(self, new_name):
        for label in self.labels:
            if label.name == new_name:
                error = QErrorMessage()
                error.showMessage(f"The label {new_name} already exists !")
                error.exec_()
                return True
        return False

    def create_label(self):
        dialog = QInputDialog(self.main_ui)
        QInputDialog.setInputMode(dialog, QInputDialog.TextInput)
        dialog.resize(QSize(400, 200))
        dialog.setLabelText('Enter the name of the new label:')
        validate = dialog.exec_()
        name = dialog.textValue()

        if validate and not self.name_already_existing(name):
            new_label = Label(name)
            self.labels.append(new_label)
            self.main_ui.labelsWidget.add_label(new_label)

    def rename_label(self, item):
        dialog = QInputDialog(self.main_ui)
        QInputDialog.setInputMode(dialog, QInputDialog.TextInput)
        dialog.resize(QSize(400, 200))
        dialog.setLabelText(f'Rename {item.text()} label for :')
        validate = dialog.exec_()
        new_name = dialog.textValue()

        if validate and not self.name_already_existing(new_name):
            for label in self.labels:
                if label.name == item.label.name:
                    label.name = new_name
            item.setText(item.label.name)

    def del_label(self, item):
        dialogue = QMessageBox(self.main_ui)
        dialogue.setText(f"Delete {item.text()} label ?")
        dialogue.setWindowTitle("Delete labels")
        dialogue.addButton(QMessageBox.Yes)
        dialogue.addButton(QMessageBox.No)
        rep = dialogue.exec()
        if rep == QMessageBox.Yes:
            self.main_ui.labelsWidget.remove_label(item)
            for label in self.labels:
                if label == item.label:
                    self.labels.remove(label)
                    break

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QInputDialog, QMessageBox

from src.view.window.main_window import MainWindow


class LabelsController:

    def __init__(self, ui):
        self.main_ui: MainWindow = ui

    def create_label(self):
        dialog = QInputDialog(self.main_ui)
        QInputDialog.setInputMode(dialog, QInputDialog.TextInput)
        dialog.resize(QSize(400, 200))
        dialog.setLabelText('Enter the name of the new label:')
        validate = dialog.exec_()
        text = dialog.textValue()
        if validate:
            print(text)

    def rename_label(self, item):
        dialog = QInputDialog(self.main_ui)
        QInputDialog.setInputMode(dialog, QInputDialog.TextInput)
        dialog.resize(QSize(400, 200))
        dialog.setLabelText(f'Rename {item.text()} debug for :')
        validate = dialog.exec_()
        text = dialog.textValue()
        if validate:
            item.setText(text)

    def del_label(self, item):
        dialogue = QMessageBox(self.main_ui)
        dialogue.setText(f"Delete {item.text()} label ?")
        dialogue.setWindowTitle("Delete labels")
        dialogue.addButton(QMessageBox.Yes)
        dialogue.addButton(QMessageBox.No)
        rep = dialogue.exec()
        if rep == QMessageBox.Yes:
            print("del ", item.text())

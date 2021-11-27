from PyQt5.QtCore import pyqtSlot, QSize
from PyQt5.QtGui import QWindow
from PyQt5.QtWidgets import QApplication, QInputDialog

from src.model.labels import Labels
from src.view.window.main_window import MainWindow


class ImageAnnotatorController:
    labels: Labels
    app: QApplication
    main_ui: MainWindow

    def __init__(self):
        self.labels = Labels(self)

    def set_ui(self, ui):
        self.main_ui = ui

    def create_label(self):
        dialog = QInputDialog(self.main_ui)
        QInputDialog.setInputMode(dialog, QInputDialog.TextInput)
        dialog.resize(QSize(400, 200))
        dialog.setLabelText('Enter the name of the new label:')
        validate = dialog.exec_()
        text = dialog.textValue()
        if validate:
            print(text)

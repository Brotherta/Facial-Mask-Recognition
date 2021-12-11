from PyQt5.QtCore import Qt
from PyQt5.QtGui import QWindow
from PyQt5.QtWidgets import QDialog, QProgressBar, QPushButton, QVBoxLayout, QLabel, QWidget, QMainWindow

from src.view.window import EditorWindow


class ProgressLoad(QDialog):

    def __init__(self, editorWindow: QMainWindow):
        super().__init__(parent=editorWindow)
        self.setWindowTitle("Importing images. Please wait.")
        self.layout = QVBoxLayout()
        self.adjustSize()
        self.labelNbToLoad = QLabel(self)
        self.currentLoading = QLabel(self)
        self.progress = QProgressBar(self)
        self.progress.setGeometry(200, 80, 250, 20)
        self.cancel = QPushButton("Cancel import", self)

        self.layout.addWidget(self.labelNbToLoad)
        self.layout.addWidget(self.currentLoading)
        self.layout.addWidget(self.progress)
        self.layout.addWidget(self.cancel)
        self.setLayout(self.layout)

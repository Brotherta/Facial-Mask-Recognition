from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton

from src.data.DataContainer import DataContainer
from src.view.widget.ProjectWindow import ProjectWidget

TITLE = "Welcome to Image Annotator"


class ProjectWindow(QMainWindow):
    def __init__(self):
        super(ProjectWindow, self).__init__()

        self.setWindowTitle(TITLE)
        self.setWindowIcon(QIcon("assets/icon.png"))
        self.setFixedSize(900, 450)
        self.widget = QWidget()
        self.layout = QVBoxLayout()
        self.widget.setLayout(self.layout)

        self.projectWidget = ProjectWidget()
        self.buttonWidget = QWidget()
        layoutButtons = QHBoxLayout()
        self.buttonWidget.setLayout(layoutButtons)

        self.newProjectButton = QPushButton("New project", self)
        self.importProjectButton = QPushButton("Import existing project", self)
        layoutButtons.addWidget(self.newProjectButton)
        layoutButtons.addWidget(self.importProjectButton)

        self.layout.addWidget(self.buttonWidget)
        self.layout.addWidget(self.projectWidget)

        self.setCentralWidget(self.widget)



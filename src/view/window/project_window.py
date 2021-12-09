from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton

from src.model.project import Project
from src.view.widget.project_widget import ProjectWidget

TITLE = "Welcome to Image Annotator"


class ProjectWindow(QMainWindow):
    def __init__(self):
        super(ProjectWindow, self).__init__()

        self.setWindowTitle(TITLE)
        self.setFixedSize(900, 450)
        self.widget = QWidget()
        self.layout = QVBoxLayout()
        self.widget.setLayout(self.layout)

        self.projectWidget = ProjectWidget()
        self.buttonWidget = QWidget()
        layout_buttons = QHBoxLayout()
        self.buttonWidget.setLayout(layout_buttons)

        self.new_project_button = QPushButton("New project", self)
        self.import_project_button = QPushButton("Import existing project", self)
        layout_buttons.addWidget(self.new_project_button)
        layout_buttons.addWidget(self.import_project_button)

        self.layout.addWidget(self.buttonWidget)
        self.layout.addWidget(self.projectWidget)

        self.setCentralWidget(self.widget)


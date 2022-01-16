from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSizePolicy

from src.view.widget.ProjectWidget import ProjectWidget

TITLE = "Welcome to Image Annotator"

'''
In this window, the user has to choose the project to work with.
We are using 2 layouts, first a horizontal layout, which is on the top of the window, containing the new and import buttons
Secondly, a vertical layout, above the first one, which contain the project list.
'''


class ProjectWindow(QMainWindow):
    def __init__(self):
        super(ProjectWindow, self).__init__()

        self.setWindowTitle(TITLE)
        self.setWindowIcon(QIcon("assets/icon.png"))
        self.setFixedSize(900, 450)

        self.widget = QWidget()  # Main widget of the window
        self.layout = QVBoxLayout()  # Main layout of the window
        self.widget.setLayout(self.layout)

        self.bottomLayout = QHBoxLayout()
        self.bottomWidget = QWidget()
        self.bottomWidget.setLayout(self.bottomLayout)

        self.projectWidget = ProjectWidget()
        self.buttonWidget = QWidget()
        layoutButtons = QHBoxLayout()  # Horizontal layout just for the buttons
        self.buttonWidget.setLayout(layoutButtons)

        self.rightWidget = QLabel(self)
        pixmap = QPixmap("assets/icon.png")
        self.rightWidget.setPixmap(pixmap)

        # Buttons
        self.newProjectButton = QPushButton("New project", self)
        self.importProjectButton = QPushButton("Import existing project", self)
        layoutButtons.addWidget(self.newProjectButton)
        layoutButtons.addWidget(self.importProjectButton)

        self.bottomLayout.addWidget(self.projectWidget)
        self.bottomLayout.addWidget(self.rightWidget)

        self.layout.addWidget(self.buttonWidget)
        self.layout.addWidget(self.bottomWidget)


        self.setCentralWidget(self.widget)

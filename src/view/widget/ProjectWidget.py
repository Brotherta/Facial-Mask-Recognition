from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QListWidget, QAction, QListWidgetItem

from src.model.Project import Project
from utils import utils

'''
The project list widget.

'''


class ProjectWidget(QListWidget):
    keyPressSignal = QtCore.pyqtSignal(int)

    def __init__(self):
        super(ProjectWidget, self).__init__()
        self.setStyleSheet(utils.load_stylesheet('style/labels.css'))  # Apply our custom CSS stylesheet
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy(Qt.ScrollBarAlwaysOff))  # Adding a crossbar if needed
        self.setSpacing(5)
        self.setMaximumWidth(437)  # We want that the list take half of the window, in the left

        self.setContextMenuPolicy(Qt.ActionsContextMenu)  # Allow right click contextual menu
        self.openProjectAction = QAction("Open project", self)
        self.deleteProjectAction = QAction("Delete project", self)

        '''
        Adding the actions to the widget. Since we set the ActionsContextMenu policy, they will be shown on right click
        '''
        self.addActions([self.openProjectAction, self.deleteProjectAction])

    # Add a new project to the widget (on the list)
    def addProject(self, project: Project):
        newProject = ProjectItem(project)
        self.addItem(newProject)

    # Remove a project of the widget
    def removeProject(self, item):
        self.takeItem(self.row(item))

    # Register keypress event, here it will be for the delete key
    def keyPressEvent(self, e: QtGui.QKeyEvent) -> None:
        self.keyPressSignal.emit(e.key())


# A Custom QListWidgetItem, which is initialised from a Project Object
class ProjectItem(QListWidgetItem):

    def __init__(self, project: Project):
        super(ProjectItem, self).__init__()
        self.project = project
        self.description = self.project.name + ": " + self.project.path # Getting the project name and path
        self.setText(self.description)  # Apply the name to the widget
        self.setToolTip(self.description)  # When the mouse hover the item
        self.setTextAlignment(Qt.AlignLeft)

    @property
    def name(self):
        return self.project.name

    @property
    def path(self):
        return self.project.path

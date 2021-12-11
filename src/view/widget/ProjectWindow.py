from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QListWidget, QAction, QListWidgetItem

from src.model.Project import Project
from utils import utils


class ProjectWidget(QListWidget):
    keyPressSignal = QtCore.pyqtSignal(int)

    def __init__(self):
        super(ProjectWidget, self).__init__()
        self.setStyleSheet(utils.load_stylesheet('style/labels.css'))
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy(Qt.ScrollBarAlwaysOff))
        self.setSpacing(5)
        self.setMaximumWidth(437)

        self.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.openProjectAction = QAction("Open project", self)
        self.deleteProjectAction = QAction("Delete project", self)
        self.addActions([self.openProjectAction, self.deleteProjectAction])

    def addProject(self, project: Project):
        newProject = ProjectItem(project)
        self.addItem(newProject)

    def removeProject(self, item):
        self.takeItem(self.row(item))

    def keyPressEvent(self, e: QtGui.QKeyEvent) -> None:
        self.keyPressSignal.emit(e.key())


class ProjectItem(QListWidgetItem):

    def __init__(self, project: Project):
        super(ProjectItem, self).__init__()
        self.project = project
        self.description = self.project.name + ": " + self.project.path
        self.setText(self.description)
        self.setToolTip(self.description)
        self.setTextAlignment(Qt.AlignLeft)

    @property
    def name(self):
        return self.project.name

    @property
    def path(self):
        return self.project.path

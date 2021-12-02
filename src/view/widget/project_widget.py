from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QAction

from src.model.project import Project
from utils import utils


class ProjectWidget(QListWidget):
    keyPress = QtCore.pyqtSignal(int)

    def __init__(self):
        super(ProjectWidget, self).__init__()
        self.setStyleSheet(utils.load_stylesheet('style/labels.css'))
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy(Qt.ScrollBarAlwaysOff))
        self.setSpacing(5)
        self.setMaximumWidth(500)

        self.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.open_project_action = QAction("Open project", self)
        self.delete_project_action = QAction("Delete project", self)
        self.addActions([self.open_project_action, self.delete_project_action])

    def add_project(self, project: Project):
        new_project = ProjectItem(project)
        self.addItem(new_project)

    def remove_project(self, item):
        self.takeItem(self.row(item))

    def keyPressEvent(self, e: QtGui.QKeyEvent) -> None:
        self.keyPress.emit(e.key())




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

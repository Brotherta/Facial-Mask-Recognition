import configparser
import os

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QErrorMessage, QFileDialog

from src.data.DataContainer import DataContainer
from src.model.Project import Project
from src.view.widget.NewProject import NewProjectDialog
from src.view.widget.ProjectWidget import ProjectItem
from src.view.window.MainWindow import MainWindow
from src.view.window.ProjectWindow import ProjectWindow


class ProjectController:
    def __init__(self, mainWindow: MainWindow, projectWindow: ProjectWindow, data: DataContainer):
        self.data = data
        self.mainWindow = mainWindow
        self.projectWindow = projectWindow

    def createProject(self):
        newProjectDialog = NewProjectDialog(self.projectWindow)
        newProjectDialog.validateButton.clicked.connect(
            lambda: self.validateCreated(newProjectDialog)
        )
        newProjectDialog.pathButton.clicked.connect(
            lambda: self.chooseDirectory(newProjectDialog)
        )
        newProjectDialog.cancelButton.clicked.connect(
            lambda: self.cancelCreated(newProjectDialog)
        )
        newProjectDialog.exec_()

    def validateCreated(self, dialog: NewProjectDialog):
        name = dialog.projectName.text()
        path = dialog.projectPath.text()
        if len(path) != 0 and len(name) != 0:
            newProject = Project(name, path)
            newProject.createConfig()
            newProject.saveConfig()
            self.data.projects.append(newProject)
            self.projectWindow.projectWidget.addProject(newProject)
            dialog.close()
        elif len(path) == 0:
            error = QErrorMessage(dialog)
            error.showMessage(f"You must choose a directory for the project !")
            error.exec()
        else:
            error = QErrorMessage(dialog)
            error.showMessage(f"You must enter a name for the  project !")
            error.exec()

    def chooseDirectory(self, dialog: NewProjectDialog):
        filepath = QFileDialog.getExistingDirectory(parent=self.projectWindow, caption="Choose an empty directory")
        if filepath != '':
            if os.listdir(filepath):
                error = QErrorMessage(dialog)
                error.showMessage(f"{filepath} directory is not empty !")
                error.exec()
            else:
                dialog.projectPath.setText(filepath)

    @staticmethod
    def cancelCreated(dialog: NewProjectDialog):
        dialog.close()

    def deleteProject(self, item: ProjectItem):
        project = item.project
        project.delete()
        self.projectWindow.projectWidget.removeProject(item)

    def importProject(self):
        projectIniFilePath, _ = QFileDialog.getOpenFileName(parent=self.projectWindow,
                                                            caption="Choose a project.ini file",
                                                            filter="Init files (project.ini)")
        if projectIniFilePath != "":
            projectConfig = configparser.ConfigParser()
            projectConfig.read(projectIniFilePath)
            try:
                name = projectConfig['PROJECT']['name']
                filepath = projectConfig['PROJECT']['filepath']

                importedProject = Project(name, filepath)
                importedProject.config = projectConfig
                importedProject.saveConfig()

                self.projectWindow.projectWidget.addProject(importedProject)

            except KeyError:
                error = QErrorMessage(self.projectWindow)
                error.showMessage(f"The selected project is corrupted or not correct.")
                error.exec()


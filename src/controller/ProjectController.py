import configparser
import os

from PyQt5.QtWidgets import QErrorMessage, QFileDialog

from src.data.DataContainer import DataContainer
from src.model.Project import Project
from src.view.widget.NewProject import NewProjectDialog
from src.view.widget.ProjectWidget import ProjectItem
from src.view.window.MainWindow import MainWindow
from src.view.window.ProjectWindow import ProjectWindow


# This is the controller for all project manipulations.
class ProjectController:
    def __init__(self, mainWindow: MainWindow, projectWindow: ProjectWindow, data: DataContainer):
        self.data = data
        self.mainWindow = mainWindow
        self.projectWindow = projectWindow

    def createProject(self):
        """ Open a new project dialog. """
        newProjectDialog = NewProjectDialog(self.projectWindow)

        # Assigns buttons events
        newProjectDialog.validateButton.clicked.connect(
            lambda: self.validateCreated(newProjectDialog)
        )
        newProjectDialog.pathButton.clicked.connect(
            lambda: self.chooseDirectory(newProjectDialog)
        )
        newProjectDialog.cancelButton.clicked.connect(
            lambda: self.cancelCreated(newProjectDialog)
        )

        newProjectDialog.exec_()  # Launch the dialog

    def validateCreated(self, dialog: NewProjectDialog):
        """ New project dialog validate button click event. """
        # Getting project description
        name = dialog.projectName.text()
        path = dialog.projectPath.text()

        # The description is valid, create the project object
        if len(path) != 0 and len(name) != 0:
            newProject = Project(name, path)
            newProject.createConfig()
            newProject.saveConfig()

            self.data.projects.append(newProject)  # Add the project to the global data container
            self.projectWindow.projectWidget.addProject(newProject)  # Add the project to the widget list of the window
            dialog.close()  # Work finished, close the dialog

        # If the description is invalid
        elif len(path) == 0:
            error = QErrorMessage(dialog)
            error.showMessage(f"You must choose a directory for the project !")
            error.exec()
        else:
            error = QErrorMessage(dialog)
            error.showMessage(f"You must enter a name for the  project !")
            error.exec()

    def chooseDirectory(self, dialog: NewProjectDialog):
        """ Open the file explorer to choose a directory. """
        filepath = QFileDialog.getExistingDirectory(parent=self.projectWindow, caption="Choose an empty directory")
        if filepath != '':
            if os.listdir(filepath):
                error = QErrorMessage(dialog)
                error.showMessage(f"{filepath} directory is not empty !")
                error.exec()
            else:
                dialog.projectPath.setText(filepath)  # The filepath is valid, assign the value to the widget

    @staticmethod
    def cancelCreated(dialog: NewProjectDialog):
        """ New project dialog cancel button clicked event. """
        dialog.close()  # Simply close the dialog

    def deleteProject(self, item: ProjectItem):
        """ Delete a project from the widget list and the configurations files. """
        project = item.project
        project.delete()  # Delete from the configurations files
        self.projectWindow.projectWidget.removeProject(item)  # Delete from the widget

    def importProject(self):
        """ Open the file explorer to choose and already created project directory. """
        projectIniFilePath, _ = QFileDialog.getOpenFileName(parent=self.projectWindow,
                                                            caption="Choose a project.ini file",
                                                            filter="Init files (project.ini)")
        if projectIniFilePath != "":  # Valid path
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


import os

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QInputDialog, QFileDialog, QErrorMessage

from src.model.project import Project
from src.view.widget.new_project import NewProjectDialog
from src.view.widget.project_widget import ProjectItem
from src.view.window.project_window import ProjectWindow



class ProjectsController:

    def __init__(self, project_ui, main_ui):
        self.project_ui: ProjectWindow = project_ui
        self.main_ui = main_ui
        self.projects: list[Project] = []

    def create_project(self):
        new_project_dialog = NewProjectDialog(self.project_ui)
        new_project_dialog.validate_button.clicked.connect(
            lambda: self.validate_created(new_project_dialog)
        )
        new_project_dialog.path_button.clicked.connect(
            lambda: self.choose_directory(new_project_dialog)
        )
        new_project_dialog.cancel_button.clicked.connect(
            lambda: self.cancel_created(new_project_dialog)
        )
        new_project_dialog.exec_()

    def choose_directory(self, dialog: NewProjectDialog):
        filepath = QFileDialog.getExistingDirectory(parent=self.project_ui, caption="Choose an empty directory")
        if os.listdir(filepath):
            error = QErrorMessage(dialog)
            error.showMessage(f"{filepath} directory is not empty !")
            error.exec()
        else:
            dialog.project_path.setText(filepath)

    def validate_created(self, dialog: NewProjectDialog):
        name = dialog.project_name.text()
        path = dialog.project_path.text()
        if len(path) != 0 and len(name) != 0:
            new_project = Project(name, path)
            new_project.create_config()
            self.projects.append(new_project)
            self.project_ui.projectWidget.add_project(new_project)
            dialog.close()
        elif len(path) == 0:
            error = QErrorMessage(dialog)
            error.showMessage(f"You must choose a directory for the project !")
            error.exec()
        else:
            error = QErrorMessage(dialog)
            error.showMessage(f"You must enter a name for the  project !")
            error.exec()

    def cancel_created(self, dialog: NewProjectDialog):
        dialog.close()
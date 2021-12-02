import configparser
import json
import os

from src import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QInputDialog, QFileDialog, QErrorMessage

from src.model.project import Project
from src.view.widget.new_project import NewProjectDialog
from src.view.widget.project_widget import ProjectItem
from src.view.window.project_window import ProjectWindow



class ProjectsController:

    def __init__(self, project_ui, main_ui, main_controller):
        self.main_controller = main_controller
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

    def delete_project(self, item):
        with open('projects.json', 'r') as f:
            config = json.load(f)
            f.close()
        config['projects'].remove(item.project.config_path)
        with open('projects.json', 'w') as f:
            f.seek(0)
            f.write(json.dumps(config, sort_keys=True, indent=4))
            f.close()
        self.project_ui.projectWidget.remove_project(item)


    def choose_directory(self, dialog: NewProjectDialog):
        filepath = QFileDialog.getExistingDirectory(parent=self.project_ui, caption="Choose an empty directory")
        if filepath != '':
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
            self.save_project_config(new_project)
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

    def save_project_config(self, project):
        with open('projects.json', 'r') as f:
            old_config = json.load(f)
            f.flush()
            f.close()

        old_config['projects'].append(project.config_path)

        with open('projects.json', 'w') as f:
            f.seek(0)
            f.write(json.dumps(old_config, sort_keys=True, indent=4))
            f.truncate()
            f.flush()
            f.close()

    def import_project(self):
        project_ini, _ = QFileDialog.getOpenFileName(parent=self.project_ui, caption="Choose a project.ini file", filter="Init files (project.ini)")

        if project_ini != "":
            project_config = configparser.ConfigParser()
            project_config.read(project_ini)
            try:
                name = project_config['PROJECT']['name']
                filepath = project_config['PROJECT']['filepath']
                imported_project = Project(name, filepath)
                imported_project.config = project_config
                self.project_ui.projectWidget.add_project(imported_project)

                self.save_project_config(imported_project)
            except KeyError:
                error = QErrorMessage(self.project_ui)
                error.showMessage(f"The selected project is corrupted or not correct.")
                error.exec()

    def keyPressHandler(self, key: QtGui.QKeyEvent):
        if key == Qt.Key_Delete:
            self.delete_project(self.project_ui.projectWidget.currentItem())
        if key == Qt.Key_Enter:
            self.main_controller.open_project()

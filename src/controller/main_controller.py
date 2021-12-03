import configparser
import json
import os
from types import TracebackType

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QErrorMessage

from src.controller.images_controller import ImagesController
from src.controller.labels_controller import LabelsController
from src.controller.menu_controller import MenuController
from src.controller.projects_controller import ProjectsController
from src.model.label import Label
from src.model.project import Project
from src.view.widget.labels_widget import LabelsListWidget
from src.view.widget.project_widget import ProjectWidget
from src.view.window.main_window import MainWindow
from src.view.window.project_window import ProjectWindow


class ImageAnnotatorController:

    def __init__(self, ui, ui_project):
        self.project = None
        self.config = None
        self.main_ui: MainWindow = ui
        self.ui_project: ProjectWindow = ui_project
        self.menu_controller = MenuController(ui)
        self.labels_controller = LabelsController(ui)
        self.images_controller = ImagesController(ui, self)
        self.projects_controller = ProjectsController(ui_project, ui, self)
        self.load_config()

        self.connect_event_menu_bar()
        self.connect_event_label_widget()
        self.connect_event_images_widget()
        self.connect_event_project_widget()

    def connect_event_project_widget(self):

        self.ui_project.new_project_button.clicked.connect(
            self.projects_controller.create_project
        )
        self.ui_project.projectWidget.itemDoubleClicked.connect(
            lambda: self.open_project(self.ui_project.projectWidget.currentItem().project)
        )
        self.ui_project.import_project_button.clicked.connect(
            self.projects_controller.import_project
        )
        self.ui_project.projectWidget.delete_project_action.triggered.connect(
            lambda: self.projects_controller.delete_project(self.ui_project.projectWidget.currentItem())
        )
        self.ui_project.projectWidget.open_project_action.triggered.connect(
            lambda: self.open_project(self.ui_project.projectWidget.currentItem().project)
        )
        self.ui_project.projectWidget.keyPress.connect(
            self.projects_controller.keyPressHandler
        )

    def connect_event_menu_bar(self):
        self.main_ui.menuBar.save_menu.triggered.connect(lambda: self.save_project())

    def connect_event_label_widget(self):
        labels_widget = self.main_ui.labelsWidget
        del_action = labels_widget.delete_item_action
        rename_action = labels_widget.rename_item_action
        create_action = labels_widget.create_item_action

        self.main_ui.menuBar.new_label.triggered.connect(
            self.labels_controller.create_label
        )
        labels_widget.itemDoubleClicked.connect(
            self.labels_controller.rename_label
        )
        rename_action.triggered.connect(
            lambda: self.labels_controller.rename_label(labels_widget.currentItem())
        )
        del_action.triggered.connect(
            lambda: self.labels_controller.del_label(labels_widget.currentItem())
        )
        labels_widget.delEvent.connect(
            lambda: self.labels_controller.del_label(labels_widget.currentItem())
        )
        create_action.triggered.connect(self.labels_controller.create_label)

    def connect_event_images_widget(self):
        images_widget = self.main_ui.imagesWidget
        images_widget.itemDoubleClicked.connect(
            lambda: self.images_controller.on_image_click(images_widget.currentItem())
        )
        self.main_ui.menuBar.import_image.triggered.connect(
            lambda: self.images_controller.load_new_image()
        )

    def load_project(self, project: Project):
        self.set_project(project)
        image_folder = project.config['PROJECT']['images']
        images = os.listdir(image_folder)
        #self.images_controller.load_images(images, image_folder)
        self.labels_controller.set_labels(self.project.load_labels())
        self.images_controller.load_images(self.project.load_images())

    def save_project(self):
        self.project.save_labels(self.labels_controller.labels)
        self.project.save_images(self.images_controller.images)

    def set_project(self, project: Project):
        self.project = project

    def open_project(self, project: Project):
        self.ui_project.close()
        self.load_project(project)
        self.main_ui.show()

    def load_config(self):
        try:
            with open('projects.json', 'r') as f:
                self.config = json.load(f)
                f.close()
                projects_list = self.config['projects']
                projects = []
                error = False
                for project in projects_list:
                    try:
                        project_config = configparser.ConfigParser()
                        project_config.read(project)
                        name = project_config['PROJECT']['name']
                        path = project_config['PROJECT']['filepath']
                        project = Project(name, path)
                        project.config = project_config

                        self.ui_project.projectWidget.add_project(project)
                    except KeyError:
                        error = QErrorMessage()
                        error.showMessage(f"project {project} has been deleted or moved !")
                        error.exec_()

                        self.config['projects'].remove(project)

                        with open('projects.json', 'w') as f2:
                            f2.seek(0)
                            f2.write(json.dumps(self.config, sort_keys=True, indent=4))
                            f2.truncate()
                            f2.flush()
                            f2.close()



        except FileNotFoundError:
            with open('projects.json', 'w') as f:
                self.config = {
                    "projects": []
                }
                f.write(json.dumps(self.config, sort_keys=True, indent=4))
                f.close()
        except KeyError as e:
            print(e.with_traceback())



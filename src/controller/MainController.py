import configparser
import json
import traceback
import webbrowser

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWidgets import QErrorMessage, QMessageBox
from importlib_metadata import sys
from qt_material import apply_stylesheet

from src.controller.ImagesController import ImagesController
from src.controller.LabelsController import LabelsController
from src.controller.ProjectController import ProjectController
from src.controller.ModelsController import ModelsController
from src.data.DataContainer import DataContainer
from src.model.Label import LabelEncoder
from src.model.Project import Project
from src.view.window.MainWindow import MainWindow
from src.view.window.ProjectWindow import ProjectWindow
from src.view.widget.MenuWidget import MenuBar

# This is the main controller of the program. The main root.
class MainController:

    def __init__(self, app, mainWindow: MainWindow, projectWindow: ProjectWindow, data: DataContainer):
        self.config = None
        self.data = data
        self.mainWindow = mainWindow
        self.projectWindow = projectWindow
        self.openedProject: Project
        self.app = app

        self.loadConfigs()  # Load program config and history

        # Load sub controllers
        self.projectController = ProjectController(mainWindow, projectWindow, data)
        self.labelsController = LabelsController(mainWindow, data)
        self.imagesController = ImagesController(mainWindow, data)
        self.modelsController = ModelsController(mainWindow, data)
        

        # Connect widgets events to their actions
        self.connectEventProjectWidget()
        self.connectEventLabelsWidget()
        self.connectEventMenuBar()
        self.connectEventImagesWidget()

    def connectEventImagesWidget(self):
        """ Connects events related to the images list widget. """

        imagesWidget = self.mainWindow.imagesWidget
        imagesWidget.itemDoubleClicked.connect(
            lambda: self.imagesController.openEditor(imagesWidget.currentItem())
        )
        self.mainWindow.menuBar.importImage.triggered.connect(
            lambda: self.imagesController.loadNewImage()
        )
        imagesWidget.delKeyPressSignal.connect(
            lambda: self.imagesController.delete(imagesWidget.selectedItems())
        )
        imagesWidget.deleteAction.triggered.connect(
            lambda: self.imagesController.delete(imagesWidget.selectedItems())
        )
        self.mainWindow.closeEventSignal.connect(
            self.closeEventHandler
        )

    def connectEventProjectWidget(self):
        """ Connects events related to the project window. """

        # Opens a project from double-clicking a menu.
        self.projectWindow.projectWidget.itemDoubleClicked.connect(
            lambda: self.openProject(
                self.projectWindow.projectWidget.currentItem().project
            )
        )
        # Opens a project from the context menu.
        self.projectWindow.projectWidget.openProjectAction.triggered.connect(
            lambda: self.openProject(
                self.projectWindow.projectWidget.currentItem().project
            )
        )
        # Imports a project from import button.
        self.projectWindow.importProjectButton.clicked.connect(
            self.projectController.importProject
        )
        # Creates a project from create button.
        self.projectWindow.newProjectButton.clicked.connect(
            self.projectController.createProject
        )
        # Deletes a project from history from delete menu.
        self.projectWindow.projectWidget.deleteProjectAction.triggered.connect(
            lambda: self.projectController.deleteProject(
                self.projectWindow.projectWidget.currentItem()
            )
        )
        # Connects the key pressed signal.
        self.projectWindow.projectWidget.keyPressSignal.connect(
            self.keyPressHandler
        )

    def connectEventLabelsWidget(self):
        """ Connects events related to the labels widget. """

        labelsWidget = self.mainWindow.labelsWidget
        deleteAction = labelsWidget.deleteItemAction
        renameAction = labelsWidget.renameItemAction
        createAction = labelsWidget.createItemAction

        self.mainWindow.menuBar.newLabel.triggered.connect(
            self.labelsController.createLabel
        )
        labelsWidget.itemDoubleClicked.connect(
            self.labelsController.renameLabel
        )
        renameAction.triggered.connect(
            lambda: self.labelsController.renameLabel(labelsWidget.currentItem())
        )
        deleteAction.triggered.connect(
            lambda: self.labelsController.deleteLabel(labelsWidget.selectedItems())
        )
        labelsWidget.delSignal.connect(
            lambda: self.labelsController.deleteLabel(labelsWidget.selectedItems())
        )
        createAction.triggered.connect(self.labelsController.createLabel)

    def connectEventMenuBar(self):
        """ Connects events related to the bar menu. """
        menuBar: MenuBar = self.mainWindow.menuBar

        self.mainWindow.menuBar.saveMenu.triggered.connect(
            self.saveEvent
        )
        self.mainWindow.menuBar.setLightMode.triggered.connect(
            self.switchLightMode
        )
        self.mainWindow.menuBar.setDarkMode.triggered.connect(
            self.switchDarkMode
        )
        self.mainWindow.menuBar.helpUse.triggered.connect(
            self.about
        )
        self.mainWindow.menuBar.importLabels.triggered.connect(
            self.labelsController.importLabels
        )
        menuBar.createModel.triggered.connect(
            self.modelsController.createModel
        )
        menuBar.createModelExisting.triggered.connect(
            self.modelsController.createModelExisting
        )
        menuBar.loadModel.triggered.connect(
            self.modelsController.loadModel
        )
        menuBar.predictImage.triggered.connect(
            self.modelsController.predictImage
        )
        menuBar.stopTraining.triggered.connect(
            self.modelsController.cancelTraining
        )

    def switchLightMode(self):
        """ Switch the program into light mode theme """
        apply_stylesheet(self.app, theme='light_purple.xml')

    def switchDarkMode(self):
        """ Switch the program into dark mode theme """
        apply_stylesheet(self.app, theme='dark_purple.xml')

    def openProject(self, project: Project):
        """ Assign the given project into a current project state for the program. """
        self.projectWindow.close()  # Close the project choice window.

        # Load project
        self.data.project = project  # Set current project
        project.loadProject(self.data)  # Load

        # Load the main window widgets
        self.labelsController.setLabels()
        self.imagesController.loadImages()
        self.mainWindow.show()  # Show the window

    def loadConfigs(self):
        """ Loads the config in projects.json and get the history of all existing project """
        try:
            with open('projects.json', 'r') as f:
                self.config = json.load(f)
                f.flush()
                f.close()
                projectsList = self.config['projects']
                for project in projectsList:
                    try:
                        projectConfig = configparser.ConfigParser()
                        projectConfig.read(project)
                        name = projectConfig['PROJECT']['name']
                        path = projectConfig['PROJECT']['filepath']
                        project = Project(name, path)
                        project.config = projectConfig

                        self.projectWindow.projectWidget.addProject(project)
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
            print(e, traceback.format_exc())

    def keyPressHandler(self, key: QtGui.QKeyEvent):
        """ Catch delete key of the project window, to delete project, or enter/return to open. """
        if key == Qt.Key_Delete:
            self.projectController.deleteProject(self.projectWindow.projectWidget.currentItem())
        if key == Qt.Key_Enter or key == Qt.Key_Return:
            self.openProject(self.projectWindow.projectWidget.currentItem().project)

    def saveEvent(self):
        """ Save the data container into their files and informs it to the user. """
        self.data.project.saveProject(self.data)
        msg = QMessageBox()
        msg.setText("We saved everything !\nYou can now close the program if you want.")
        msg.setWindowTitle("Saved.")
        msg.setIcon(QMessageBox.Information)
        msg.exec_()

    def getSavedState(self) -> bool:
        """ Compare the current data hash with the initial hash at the loading moment. """
        dumpedLabels = json.dumps(self.data.labels, indent=4, cls=LabelEncoder)
        dumpedImages = json.dumps(self.data.images, indent=4, cls=LabelEncoder)
        concatenatedSave = dumpedLabels + dumpedImages
        return concatenatedSave == self.data.project.concatenatedSaves

    def closeEventHandler(self, event: QtGui.QCloseEvent) -> None:
        """ When the user try to close the event, we catch the event and ask the user to save or not if needed. """
        # If there is no data which need to be saved
        if self.getSavedState():
            event.accept()
        else:
            # Ask to the user
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Do you want to save before leaving ?")
            msg.setWindowTitle("Existing unsaved work")
            msg.setStandardButtons(QMessageBox.Save | QMessageBox.No | QMessageBox.Cancel)

            value = msg.exec_()
            if value == QMessageBox.Save:
                self.data.project.saveProject(self.data)  # Save the project
                event.accept()  # Close the window
            elif value == QMessageBox.Cancel:
                event.ignore()  # The user finally doesn't want to close the window
                

    def about(self):
        """ Open the README of the github repository on the web browser. """
        webbrowser.open("https://github.com/Brotherta/Facial-Mask-Recognition/blob/main/README.md")
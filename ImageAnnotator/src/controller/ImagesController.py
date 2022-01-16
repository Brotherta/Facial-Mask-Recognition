import ntpath
import os
from threading import Thread
from time import sleep

from PIL import Image
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog, QMessageBox

from src.data.DataContainer import DataContainer
from src.model.ImageFMR import ImageFMR
from src.model.Label import Label
from src.view.widget.ImagesWidget import ImageWidgetItem
from src.view.widget.LabelDoubleClickDialog import LabelDoubleClickDialog
from src.view.widget.ProgressLoad import ProgressLoad
from src.view.window.EditorWindow import Box, EditorWidget
from src.view.window.MainWindow import MainWindow


# This is the controller for the images manipulations.
class ImagesController:

    def __init__(self, mainWindow: MainWindow, data: DataContainer):
        self.threadLoading = None
        self.progressWindow = None
        self.editorWindow = EditorWidget
        self.dialogLabelEdition = LabelDoubleClickDialog
        self.canceled = False
        self.project = None
        self.data = data
        self.mainWindow = mainWindow

    def loadNewImage(self):
        """ Open the file explorer and choose some new jpg/png images to import into the project. """
        filenames = QFileDialog.getOpenFileNames(parent=self.mainWindow, caption="Open images",
                                                 filter="Images files (*.jpg *.png)")
        if len(filenames[0]) > 0:
            # If the current OS is window, we show an asynchronous progress bar
            if os.name == 'nt':
                self.progressWindow = ProgressLoad(self.mainWindow)
                self.progressWindow.progress.setValue(0)
                self.progressWindow.show()
                self.progressWindow.progress.setMaximum(len(filenames[0]))
                self.progressWindow.cancel.clicked.connect(self.cancelLoading)
                self.threadLoading = Thread(target=self.loadWindows, args=(filenames,))  # Load images in another thread

            # We have some issues with the progress bar on macOS so we decided to not show it.
            else:
                self.threadLoading = Thread(target=self.loadMac, args=(filenames,))
            self.threadLoading.start()

    def cancelLoading(self):
        """ Notify the loading thread to cancel. """
        self.canceled = True

    def loadWindows(self, filenames):
        """ Load images function, windows version """
        self.canceled = False
        nbToDownload = len(filenames[0])
        inc = 1
        for filepath in filenames[0]:
            if self.canceled:
                break

            # Progress bar update
            self.progressWindow.labelNbToLoad.setText(f'{inc}/{nbToDownload}')
            self.progressWindow.progress.setValue(inc)
            self.progressWindow.currentLoading.setText(f"loading {filepath}")

            newFilePath = f'{self.data.project.config["PROJECT"]["images"]}/{self.getNameFromPath(filepath)}'

            # Open the image and save it to the images folder
            img = Image.open(filepath)
            img.save(f'{self.data.project.config["PROJECT"]["images"]}/{self.getNameFromPath(newFilePath)}')
            img.close()

            size = img.size
            self.addImage(ImageFMR(newFilePath, imageSize=size))  # Add the image to the data container and widget
            inc += 1

        sleep(0.1)  # Without the sleep we have somes issues with Qt.

        self.progressWindow.close()
        self.data.project.saveProjectImages(self.data)  # Save the images to the project without waiting the user.

    def loadMac(self, filenames):
        """ Load images function, macOS/Linux version. Same as above but without progress bar. """
        self.canceled = False
        inc = 1
        for filepath in filenames[0]:
            if self.canceled:
                break

            newFilePath = f'{self.data.project.config["PROJECT"]["images"]}/{self.getNameFromPath(filepath)}'

            # Open the image
            img = Image.open(filepath)
            img.save(f'{self.data.project.config["PROJECT"]["images"]}/{self.getNameFromPath(newFilePath)}')
            img.close()

            size = img.size
            self.addImage(ImageFMR(newFilePath, imageSize=size))  # Add the image to the data container and widget
            inc += 1

        sleep(0.1)  # Without the sleep we have somes issues with Qt.
        self.data.project.saveProjectImages(self.data)  # Save the images to the project without waiting the user.

    @staticmethod
    def getNameFromPath(path):
        head, tail = ntpath.split(path)
        return tail or ntpath.basename(head)

    def loadImages(self):
        """ Add all data container images to the widget. """
        for img in self.data.images:
            self.mainWindow.imagesWidget.addImage(img)

    def addImage(self, image: ImageFMR):
        """ Add a new image to the data container and the widget. """
        self.data.images.append(image)
        self.mainWindow.imagesWidget.addImage(image)

    def imageEdited(self, edited: bool, image: ImageFMR):
        """ Update the images box list if the changes are validated. """
        if edited:
            image.boxList = self.editorWindow.imageLabel.boxListTemp
        self.editorWindow.close()

    def openEditor(self, item: ImageWidgetItem):
        """ Open the image editor window. """
        self.editorWindow = EditorWidget(item.image, self.data.labels)
        self.editorWindow.validate.clicked.connect(lambda: self.imageEdited(True, item.image))
        self.editorWindow.cancel.clicked.connect(lambda: self.imageEdited(False, item.image))
        self.editorWindow.imageLabel.clickOnBox.connect(self.clickOnBox)
        self.editorWindow.exec()

    def clickOnBox(self, box: Box):
        """ When a double clicked occured on a box. """
        self.dialogLabelEdition = LabelDoubleClickDialog(box, self.data.labels)
        self.dialogLabelEdition.buttonDelete.clicked.connect(lambda: self.deleteBox(box))
        self.dialogLabelEdition.buttonOk.clicked.connect(lambda: self.validateLabel(box))
        self.dialogLabelEdition.exec()

    def deleteBox(self, box: Box):
        """ Delete a box from the widgets and data lists. """
        self.editorWindow.imageLabel.boxListTemp.remove(box)
        self.editorWindow.imageLabel.scene.removeItem(box)
        self.dialogLabelEdition.close()

    def validateLabel(self, box: Box):
        """ Assign a label to the given box and set the rectangle color. """
        for l in self.data.labels:
            l: Label
            if l.name == self.dialogLabelEdition.cb.currentText():
                box.label = l
                if l.name is None:
                    box.setBrush(Qt.white)
                    box.setToolTip("None")
                else:
                    box.setBrush(Qt.darkGreen)
                    box.setToolTip(l.name)
                self.dialogLabelEdition.close()
                return

    def delete(self, items: list[ImageWidgetItem]):
        """ Delete selected images from the widget and the data container. """
        dialogue = QMessageBox(self.mainWindow)
        dialogue.setText(f"Delete {len(items)} image(s) ?")
        dialogue.setWindowTitle("Delete image(s)")
        dialogue.addButton(QMessageBox.Yes)
        dialogue.addButton(QMessageBox.No)
        rep = dialogue.exec()
        if rep == QMessageBox.Yes:
            for item in items:
                self.mainWindow.imagesWidget.takeItem(self.mainWindow.imagesWidget.row(item))
                self.data.images.remove(item.image)

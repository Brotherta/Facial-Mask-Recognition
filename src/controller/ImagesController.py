import ntpath
from threading import Thread
from time import sleep

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFileDialog, QInputDialog, QMessageBox, QDialog, QPushButton, QVBoxLayout, QComboBox

from src.data.DataContainer import DataContainer
from src.model.ImageFMR import ImageFMR
from src.model.Label import Label
from src.view.widget.ImagesWidget import ImageWidgetItem
from src.view.widget.ProgressLoad import ProgressLoad
from src.view.window.EditorWindow import Box, EditorWidget
from src.view.window.MainWindow import MainWindow

from PIL import Image


class ImagesController:

    def __init__(self, mainWindow: MainWindow, data: DataContainer):
        self.threadLoading = None
        self.progressWindow = None
        self.editorWindow: EditorWidget
        self.canceled = False
        self.project = None
        self.data = data
        self.mainWindow = mainWindow

    def loadNewImage(self):
        filenames = QFileDialog.getOpenFileNames(parent=self.mainWindow, caption="Open images",
                                                 filter="Images files (*.jpg *.png)")
        self.progressWindow = ProgressLoad(self.mainWindow)
        self.progressWindow.progress.setValue(0)
        self.progressWindow.show()
        self.progressWindow.progress.setMaximum(len(filenames[0]))
        self.progressWindow.cancel.clicked.connect(self.cancelLoading)

        self.threadLoading = Thread(target=self.load, args=(filenames,))
        self.threadLoading.start()

    def cancelLoading(self):
        self.canceled = True

    def load(self, filenames):
        self.canceled = False
        nbToDownload = len(filenames[0])
        inc = 1
        for filepath in filenames[0]:
            if self.canceled:
                break
            self.progressWindow.labelNbToLoad.setText(f'{inc}/{nbToDownload}')
            self.progressWindow.progress.setValue(inc)
            self.progressWindow.currentLoading.setText(f"loading {filepath}")
            newFilePath = f'{self.data.project.config["PROJECT"]["images"]}/{self.getNameFromPath(filepath)}'

            img = Image.open(filepath)
            img.save(f'{self.data.project.config["PROJECT"]["images"]}/{self.getNameFromPath(newFilePath)}')
            img.close()
            size = img.size
            self.addImage(ImageFMR(newFilePath, imageSize=size))
            inc += 1
        sleep(0.1)
        self.progressWindow.close()
        self.data.project.saveProjectImages(self.data)

    @staticmethod
    def getNameFromPath(path):
        head, tail = ntpath.split(path)
        return tail or ntpath.basename(head)

    def loadImages(self):
        for img in self.data.images:
            self.mainWindow.imagesWidget.addImage(img)

    def addImage(self, image: ImageFMR):
        print("add")
        self.data.images.append(image)
        self.mainWindow.imagesWidget.addImage(image)

    def imageEdited(self, edited: bool, image: ImageFMR):
        if edited:
            image.boxList = self.editorWindow.imageLabel.boxListTemp
        self.editorWindow.close()

    def addLabelToBox(self, box: Box):
        items = list(map(lambda x: x.name, self.data.labels))
        if len(items) > 0:
            dialog = LabelDoubleClickDialog(box, self.editorWindow, self.data)
            dialog.exec_()

    def openEditor(self, item: ImageWidgetItem):
        self.editorWindow = EditorWidget(item.image, self.data.labels)
        self.editorWindow.validate.clicked.connect(lambda: self.imageEdited(True, item.image))
        self.editorWindow.cancel.clicked.connect(lambda: self.imageEdited(False, item.image))
        self.editorWindow.exec()

    def delete(self, items: list[ImageWidgetItem]):
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

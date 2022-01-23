import configparser
import json
import os
import traceback
from multiprocessing import Pipe, Process
from operator import mod
from os.path import expanduser
from threading import Thread

from PyQt5.QtWidgets import (QErrorMessage, QFileDialog, QInputDialog,
                             QMessageBox)
from src.data.DataContainer import DataContainer
from src.predictor.pipeline import Pipeline
from pre.DataPreProcessing import DataPreProcessing
from src.view.window.MainWindow import MainWindow


class ModelsController:
    def __init__(self, mainWindow: MainWindow, data: DataContainer):
        self.data = data
        self.mainWindow = mainWindow
        self.model = None
        self.t = None

    def createModel(self):
        name, ok = QInputDialog.getText(
            self.mainWindow, "Name of the model", "Enter the name of the model")

        if ok:
            filepath = QFileDialog.getOpenFileName(parent=self.mainWindow,
                                                   caption="choose annotations file",
                                                   filter="Annotations (box.json)")

            if filepath[0] != '':
                try:
                    dp = DataPreProcessing(filepath[0])
                    dp.cleanImages()  # removes previous images.

                    dp.findLabels()  # defines how many labels are in the annotations file

                    dp.crop_bounding_boxes()
                    dp.resize_moved_images()

                    dp.split_data()
                    dataImages = dp.increase_data()

                    p = Pipeline(dataImages, 30, labels=dp.labels)
                    p.make_model()


                    t = Process(target=self.trainModel, args=(p, name))
                    t.start()

                except Exception:
                    error = QErrorMessage(self.mainWindow)
                    error.showMessage(
                        "The box.json file selected is not correct or corrupted.")
                    error.exec()

    def trainModel(self, pipe, nameModel):
        pipe.fit_model(nameModel)

        msg = QMessageBox()
        msg.setText(
            f"The model {nameModel} has been trained correctly. You can load it and test it.")
        msg.setWindowTitle("Training successful.")
        msg.setIcon(QMessageBox.Information)
        msg.exec_()

    def createModelExisting(self):
        name, ok = QInputDialog.getText(
            self.mainWindow, "Name of the model", "Enter the name of the model")

        if ok:
            filepath = QFileDialog.getExistingDirectory(parent=self.mainWindow,
                                                        caption="Choose the folder images")

            if filepath is not None:
                try:
                    labels = os.listdir(filepath)

                    dp = DataPreProcessing(labels=labels)
                    dataImages = dp.split_data(filepath)

                    p = Pipeline(dataImages, 30, labels=labels)
                    p.make_model()

                    self.t = Thread(target=self.trainModel, args=(p, name))
                    self.t.start()


                except Exception as e:
                    print(e, traceback.format_exc())
                    error = QErrorMessage(self.mainWindow)
                    error.showMessage(
                        "The directory must contains subfolders of images only.")
                    error.exec()

    def cancelTraining(self):
        if self.t is not None and self.t.is_alive:
            # self.t.terminate()
            pass
        else:
            error = QErrorMessage(self.mainWindow)
            error.showMessage(
                "There is no training currently running.")
            error.exec()

    def loadModel(self):
        filepath = QFileDialog.getOpenFileName(
            parent=self.mainWindow, directory="./models", caption="Choose a model", filter="Model file (*.h5)")

        if filepath[0] != '':
            try:
                p = Pipeline()
                p.load_model(filepath[0])
                self.model = p.model

                msg = QMessageBox()
                msg.setText(
                    f"The model {filepath[0]} has been loaded correctly.")
                msg.setWindowTitle("Loading successful.")
                msg.setIcon(QMessageBox.Information)
                msg.exec_()

            except Exception as e:
                print(e, traceback.format_exc())
                error = QErrorMessage(self.mainWindow)
                error.showMessage(
                    "The model selected is not correct, please choose an other one.")
                error.exec()

    def predictImage(self):
        if self.model is not None:

            filepath = QFileDialog.getOpenFileNames(
                parent=self.mainWindow, directory=expanduser('~'), caption="Choose an image or multiple images", filter="Images files (*.png, *.jpg)")

            if filepath[0] != []:
                try:
                    p = Pipeline()
                    p.model = self.model
                    for imgPath in filepath[0]:
                        p.predict_input_image(imgPath)

                except Exception as e:
                    error = QErrorMessage(self.mainWindow)
                    error.showMessage(
                        f"An error occured:\n{e} {traceback.format_exc()}"
                    )
                    error.exec_()

        else:
            error = QErrorMessage(self.mainWindow)
            error.showMessage(
                f"There is no model loaded, please load a model."
            )
            error.exec_()

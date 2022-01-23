#!/usr/bin/env python
'''
Usage:
    ./pipeline.py  --mode [preprocess | train | predict] [--path INPUT_PATH]

'''



import shutil
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import numpy as np
import cv2
from PIL import Image
import json

import tensorflow as tf
from tensorflow.keras import layers
from tensorflow import keras


data_augmentation = keras.Sequential(
    [
        layers.RandomFlip("horizontal"),
        layers.RandomRotation(0.1)
    ]
)


class Pipeline:

    def __init__(self,
                 data=None,
                 epochs=50,
                 input_shape=(120, 120),
                 labels=['mask', 'no_mask'],
                 numClasses=2) -> None:

        self.model = None

        if data is not None:
            self.train = data[0]
            self.test = data[1]

        self.epochs = epochs
        self.input_shape = input_shape + (3,)

        self.labels = labels
        self.numClasses = numClasses

        self.net = cv2.dnn.readNetFromCaffe(
            "src/predictor/face-detection/weights-prototxt.txt", "src/predictor/face-detection/res_ssd_300Dim.caffeModel")

    def load_model(self, path=None) -> None:
        if path is None:
            path = self.model_load_path
        self.model = keras.models.load_model(path)

    def make_model(self):
        inputs = layers.Input(shape=self.input_shape)
        x = data_augmentation(inputs)

        x = layers.Conv2D(32, kernel_size=(
            3, 3), padding='same', activation='relu')(x)
        x = layers.MaxPooling2D(pool_size=(2, 2))(x)
        x = layers.Dropout(0.2)(x)

        x = layers.Conv2D(64, kernel_size=(
            3, 3), padding='same', activation='relu')(x)
        x = layers.MaxPooling2D(pool_size=(2, 2))(x)
        x = layers.Dropout(0.2)(x)

        x = layers.Conv2D(128, kernel_size=(
            3, 3), padding='same', activation='relu')(x)
        x = layers.MaxPooling2D(pool_size=(2, 2))(x)
        x = layers.Dropout(0.2)(x)

        x = layers.Conv2D(256, kernel_size=(
            3, 3), padding='same', activation='relu')(x)
        x = layers.Dropout(0.2)(x)

        x = layers.Flatten()(x)
        x = layers.Dense(256, activation='relu')(x)
        x = layers.Dense(128, activation='relu')(x)

        if self.numClasses == 2:
            outputs = layers.Dense(1, activation='sigmoid')(x)
        else:
            outputs = layers.Dense(self.numClasses, activation='softmax')(x)

        self.model = keras.Model(inputs, outputs)

    def plot_model(self) -> None:
        keras.utils.plot_model(self.model, show_shapes=True)

    def fit_model(self, name="model"):

        if self.numClasses == 2:
            self.model.compile(
                optimizer=keras.optimizers.Adam(0.001),
                loss="binary_crossentropy",
                metrics=["accuracy"],
            )

        else:
            self.model.compile(
                optimizer=keras.optimizers.Adam(0.001),
                loss="categorical_crossentropy",
                metrics=["accuracy"],
            )

        self.history = self.model.fit(
            self.train, epochs=self.epochs, validation_data=self.test
        )

        self.model.save(f"./models/{name}.h5")

    def predict_input_image(self, image_filepath) -> None:
        image = cv2.imread(image_filepath)
        (height, width) = image.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0,
                                     (300, 300), (104.0, 177.0, 123.0))

        # pass the blob into the network
        self.net.setInput(blob)
        detections = self.net.forward()

        imOut = image.copy()

        for i in range(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]

            if confidence > 0.5:
                box = detections[0, 0, i, 3:7] * \
                    np.array([width, height, width, height])
                (x1, y1, x2, y2) = box.astype("int")
                y = y1 - 10 if y1 - 10 > 10 else y1 + 10

                img = cv2.cvtColor(image[y1:y2, x1:x2], cv2.COLOR_BGR2RGB)
                img = cv2.resize(img, self.input_shape[:2])
                img = keras.preprocessing.image.img_to_array(img)
                img = tf.expand_dims(img, 0)  # Create batch axis

                predictions = self.model.predict(img)
                score = predictions[0]
                firstScore = 100 * (1 - score)
                secondScore = 100 * score

                if firstScore >= 95:
                    cv2.rectangle(imOut, (x1, y1), (x2, y2),
                                  (0, 0, 255), 1, cv2.LINE_AA)
                    cv2.putText(imOut, f"{self.labels[0]} with " + "{:.3f}%".format(
                        float(firstScore)), (x1, y), cv2.LINE_AA, 0.60, (0, 0, 255), 1,2)

                else:
                    cv2.rectangle(imOut, (x1, y1), (x2, y2),
                                  (0, 0, 255), 1, cv2.LINE_AA)
                    cv2.putText(imOut, f"{self.labels[1]} with " + "{:.3f}%".format(
                        float(secondScore)), (x1, y), cv2.LINE_AA, 0.60, (0, 0, 255), 1,2)

        cv2.imshow("Prediction", imOut)
        cv2.waitKey(0)


class DataPreProcessing:

    def __init__(self, annotationsJsonPath=None, image_size=(120, 120), batch_size=32, labels=['mask', 'no_mask']) -> None:
        self.annotationsJsonPath = annotationsJsonPath
        self.image_size = image_size
        self.batch_size = batch_size

        self.data_path_resized = "images/resized_images/"
        self.data_path_box = "images/box_images/"
        self.data_path_resized_base = "images/resized_images/"

        self.train = None
        self.test = None
        self.labels = labels

    def cleanImages(self):
        shutil.rmtree('.images')
        os.mkdir('.images')

    def run(self) -> None:
        self.cleanImages()
        self.crop_bounding_boxes()
        self.resize_moved_images()

    def findLabels(self):
        with open(self.annotationsJsonPath, 'r') as fp:
            data = json.load(fp)
            fp.flush()
            fp.close()

        self.labels = []

        for item in data:
            for box in item['boxList']:
                label = box['label']['name']
                if label is not None and label not in self.labels:
                    self.labels.append(label)

    def crop_bounding_boxes(self) -> None:
        if not os.path.exists("images"):
            os.mkdir("images")

        if not os.path.exists(self.data_path_box):
            os.mkdir(self.data_path_box)

        with open(self.annotationsJsonPath, 'r') as fp:
            data = json.load(fp)
            fp.flush()
            fp.close()

        for item in data:
            images_path = item['filepath']

            imageName = os.path.basename(images_path)

            im = Image.open(images_path)
            for box in item['boxList']:
                x = box['x']
                y = box['y']
                width = box['width']
                height = box['height']

                if box['label'] is not None:

                    label = box['label']['name']
                    path_bb = f'{self.data_path_box}/{imageName}-bb-{x}x{y}-{x+width}-{y+height}-{label}.jpg'
                    im_crop = im.crop((x, y, x+width, y+height))
                    im_crop.save(path_bb, "JPEG")

        shutil.rmtree(self.data_path_box)

    def resize_moved_images(self) -> None:

        if not os.path.exists(self.data_path_resized):
            os.mkdir(self.data_path_resized)

        for label in self.labels:
            if not os.path.exists(self.data_path_resized + label):
                os.mkdir(self.data_path_resized + label)

        boxes = os.listdir(self.data_path_box)

        acc = 0
        for box in boxes:
            im = Image.open(self.data_path_box + box)
            if im.size > self.image_size:
                acc += 1
                im.thumbnail(self.image_size, Image.ANTIALIAS)

                for label in self.labels:
                    if label in box:
                        im.save(f"{self.data_path_resized}{label}/{box}", "JPEG")

    def split_data(self, new_base=None):
        if new_base is not None:
            self.data_path_resized_base = new_base

        self.train = tf.keras.preprocessing.image_dataset_from_directory(
            self.data_path_resized_base,
            shuffle=True,
            validation_split=0.3,
            subset="training",
            seed=46,
            image_size=self.image_size,
            batch_size=self.batch_size,
        )

        self.test = tf.keras.preprocessing.image_dataset_from_directory(
            self.data_path_resized_base,
            validation_split=0.3,
            shuffle=True,
            subset="validation",
            seed=46,
            image_size=self.image_size,
            batch_size=self.batch_size,
        )

        return self.train, self.test

    def increase_data(self):
        self.train = self.train.map(
            lambda x, y: (data_augmentation(x, training=True), y))

        self.train = self.train.prefetch(buffer_size=32)
        self.test = self.test.prefetch(buffer_size=32)

        return self.train, self.test

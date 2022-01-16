#!/usr/bin/env python
'''
Usage:
    ./pipeline.py  --mode [preprocess | train | predict] [--path INPUT_PATH]

'''

import sys
import os
import numpy as np
import cv2
from PIL import Image
import json
import tensorflow as tf
from matplotlib import pyplot as plt
from tensorflow import keras
from tensorflow.keras import layers


data_augmentation = keras.Sequential(
    [
        layers.RandomFlip("horizontal"),
        layers.RandomRotation(0.1)
    ]
)



class Pipeline:
    
    model_save_path = "models/save_at_{epoch}.h5"
    model_load_path = "models/save_at_50.h5"



    def __init__(self,
                 data,
                 epochs,
                 input_shape=(120, 120),
                 activation="relu",
                 size_entry_layers=[32, 64],
                 size_block_layers=[128, 256, 512, 728],
                 size_exit_layers=1024,
                 dropout_rate=0.5,
                 dense_activation="sigmoid",
                 dropout_layer=True,
                 maxpooling_layer=True) -> None:
        

        self.model = None
        self.train = data[0]
        self.test = data[1]
        self.epochs = epochs
        self.input_shape = input_shape + (3,)
        self.size_first_layers = size_entry_layers
        self.size_block_layers = size_block_layers
        self.size_last_layers = size_exit_layers
        self.dropout_rate = dropout_rate
        self.dense_activation = dense_activation
        self.activation = activation
        self.dropout_layer = dropout_layer
        self.maxpooling_layer = maxpooling_layer

        self.net = cv2.dnn.readNetFromCaffe(
            "src/face-detection/weights-prototxt.txt", "src/face-detection/res_ssd_300Dim.caffeModel")

        # self.data_augmentation = keras.Sequential(
        #     [
        #         layers.RandomFlip("horizontal"),
        #         layers.RandomRotation(0.1)
        #     ]
        # )
        

    def load_model(self, path=model_load_path) -> None:
        self.model = keras.models.load_model(path)

    def make_model(self) -> None:
        inputs = keras.Input(shape=self.input_shape)
        # Image augmentation block
        x = data_augmentation(inputs)

        # Rescaling the input values to a new range.
        x = layers.Rescaling(scale=1.0/255)(x)

        # First layers block
        x = layers.Conv2D(
            self.size_first_layers[0], 3, strides=2, padding="same")(x)
        x = layers.BatchNormalization()(x)
        x = layers.Activation(self.activation)(x)

        x = layers.Conv2D(self.size_first_layers[1], 3, padding="same")(x)
        x = layers.BatchNormalization()(x)
        x = layers.Activation(self.activation)(x)

        # Block of layers
        previous_block_activation = x  # Set aside residual

        for size in self.size_block_layers:
            x = layers.Activation(self.activation)(x)
            x = layers.SeparableConv2D(size, 3, padding="same")(x)
            x = layers.BatchNormalization()(x)

            x = layers.Activation(self.activation)(x)
            x = layers.SeparableConv2D(size, 3, padding="same")(x)
            x = layers.BatchNormalization()(x)

            x = layers.MaxPooling2D(3, strides=2, padding="same")(x)

            # Project residual
            residual = layers.Conv2D(size, 1, strides=2, padding="same")(
                previous_block_activation
            )

            x = layers.add([x, residual])  # Add back residual
            previous_block_activation = x  # Set aside next residual

        x = layers.SeparableConv2D(self.size_last_layers, 3, padding="same")(x)
        x = layers.BatchNormalization()(x)
        x = layers.Activation(self.activation)(x)

        if self.maxpooling_layer:
            x = layers.GlobalAveragePooling2D()(x)

        if self.dropout_layer:
            x = layers.Dropout(self.dropout_rate)(x)
        
        outputs = layers.Dense(1, activation=self.dense_activation)(x)

        self.model = keras.Model(inputs, outputs)

    def plot_model(self) -> None:
        keras.utils.plot_model(self.model, show_shapes=True)

    def fit_model(self):
        callbacks = [
            keras.callbacks.ModelCheckpoint(self.model_save_path),
        ]

        self.model.compile(
            optimizer=keras.optimizers.Adam(1e-3),
            loss="binary_crossentropy",
            metrics=["accuracy"],
        )

        history = self.model.fit(
            self.train, epochs=self.epochs, callbacks=callbacks, validation_data=self.test,
        )
        
        print(history.history)

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
                img = cv2.resize(img, self.input_shape)
                img = keras.preprocessing.image.img_to_array(img)
                img = tf.expand_dims(img, 0)  # Create batch axis
                predictions = self.model.predict(img)
                score = predictions[0]
                maskScore = 100 * (1 - score)
                nomaskScore = 100 * score
                if maskScore >= 99.9:
                    cv2.rectangle(imOut, (x1, y1), (x2, y2),
                                  (0, 255, 0), 1, cv2.LINE_AA)
                    cv2.putText(imOut, "Mask with " + "{:.4f}%".format(
                        float(maskScore)), (x1, y), cv2.LINE_AA, 0.45, (0, 255, 0), 2)
                else:
                    cv2.rectangle(imOut, (x1, y1), (x2, y2),
                                  (0, 255, 0), 1, cv2.LINE_AA)
                    cv2.putText(imOut, "No_mask with " + "{:.4f}%".format(
                        float(nomaskScore)), (x1, y), cv2.LINE_AA, 0.45, (0, 255, 0), 1)

        cv2.imshow("Prediction", imOut)
        cv2.waitKey(0)


class DataPreProcessing:

    def __init__(self, annotationsJsonPath = None, image_size= None, batch_size= None) -> None:
        self.annotationsJsonPath = annotationsJsonPath
        self.image_size = image_size
        self.batch_size = batch_size

        self.data_path = "images/resized_images/"
        self.train = None
        self.test = None
        

        # self.data_augmentation = keras.Sequential(
        #     [
        #         layers.RandomFlip("horizontal"),
        #         layers.RandomRotation(0.1)
        #     ]
        # )
    
    def run(self) -> None:
        mask_path = self.data_path + "mask/"
        no_mask_path = self.data_path + "no_mask/"

        for file in os.listdir(mask_path):
            os.remove(mask_path + file)
        for file in os.listdir(no_mask_path):
            os.remove(no_mask_path + file)

        self.crop_bounding_boxes()
        self.resize_moved_images()

    def crop_bounding_boxes(self) -> None:
        if not os.path.exists("images/box_images"):
            os.mkdir("images/box_images")

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
                    path_bb = f'{"images/box_images/"}/{imageName}-bb-{x}x{y}-{x+width}-{y+height}-{label}.jpg'
                    im_crop = im.crop((x, y, x+width, y+height))
                    im_crop.save(path_bb, "JPEG")


    def resize_moved_images(self) -> None:
        
        if not os.path.exists("images/resized_images"):
            os.mkdir("images/resized_images")

        if not os.path.exists("images/resized_images/no_mask"):
            os.mkdir("images/resized_images/no_mask")

        if not os.path.exists("images/resized_images/mask"):
            os.mkdir("images/resized_images/mask")

        boxes = os.listdir("images/box_images/")

        acc = 0
        for box in boxes:
            im = Image.open("images/box_images/"+box)
            if im.size > self.image_size:
                acc += 1
                im.thumbnail(self.image_size, Image.ANTIALIAS)
                if "no_mask" in box:
                    im.save("images/resized_images/no_mask/"+box, "JPEG")
                else:
                    im.save("images/resized_images/mask/"+box, "JPEG")

        print(acc, " files resized.")

    def split_data(self):
        self.train = tf.keras.preprocessing.image_dataset_from_directory(
            self.data_path,
            validation_split=0.2,
            subset="training",
            seed=1337,
            image_size=self.image_size,
            batch_size=self.batch_size,
        )

        self.test = tf.keras.preprocessing.image_dataset_from_directory(
            self.data_path,
            validation_split=0.2,
            subset="validation",
            seed=1337,
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

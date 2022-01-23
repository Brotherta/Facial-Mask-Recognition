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
            "src/predictor/face-detection/weights-prototxt.txt", "src/predictor/face-detection/res_ssd_300Dim.caffeModel") # Load the model for the face detection

    def load_model(self, path=None) -> None:
        """Load if needed an already existing model. Or create a new one."""
        if path is None:
            path = self.model_load_path
        self.model = keras.models.load_model(path)

    def make_model(self):
        """Create our model with the parameters. The core of the training code."""
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
        """Make a plot of our model statistics."""
        keras.utils.plot_model(self.model, show_shapes=True)

    def fit_model(self, name="model"):
        """Compile the model, and compile with parameter depending on the numClasses value."""
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
        ) # Getting the statistics history of the training

        self.model.save(f"./models/{name}.h5")  # Save the model

    def predict_input_image(self, image_filepath) -> None:
        image = cv2.imread(image_filepath) # Load the image
        (height, width) = image.shape[:2]  # Get the size
        blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0,
                                     (300, 300), (104.0, 177.0, 123.0))

        # pass the blob into the network
        self.net.setInput(blob)
        detections = self.net.forward()

        imOut = image.copy() # We can draw without corrupt the original image

        for i in range(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]

            if confidence > 0.5: # Probability > 50% to be human face
                box = detections[0, 0, i, 3:7] * \
                    np.array([width, height, width, height]) # Getting the faces bounding boxes
                (x1, y1, x2, y2) = box.astype("int")
                y = y1 - 10 if y1 - 10 > 10 else y1 + 10 # This location will help us to put text above the box later

                img = cv2.cvtColor(image[y1:y2, x1:x2], cv2.COLOR_BGR2RGB) # Convert the image in order to make it keras friendly
                img = cv2.resize(img, self.input_shape[:2]) # Resize the image to the training shape (120x120 by default)
                img = keras.preprocessing.image.img_to_array(img) # Convert the image to the data array
                img = tf.expand_dims(img, 0)  # Create batch axis

                predictions = self.model.predict(img) # Call the prediction function
                score = predictions[0] # Getting the scores
                firstScore = 100 * (1 - score) # Score of mask probability
                secondScore = 100 * score # Score of no_mask probability

                if firstScore >= 95: # We want a probability > 95% for the masks
                    cv2.rectangle(imOut, (x1, y1), (x2, y2),
                                  (0, 0, 255), 1, cv2.LINE_AA) # Drawing the bounding box
                    cv2.putText(imOut, f"{self.labels[0]} with " + "{:.3f}%".format(
                        float(firstScore)), (x1, y), cv2.LINE_AA, 0.60, (0, 0, 255), 1,2) # Put the text above

                else:
                    cv2.rectangle(imOut, (x1, y1), (x2, y2),
                                  (0, 0, 255), 1, cv2.LINE_AA) # Drawing the bounding box
                    cv2.putText(imOut, f"{self.labels[1]} with " + "{:.3f}%".format(
                        float(secondScore)), (x1, y), cv2.LINE_AA, 0.60, (0, 0, 255), 1,2) # Put the text above

        cv2.imshow("Prediction", imOut) # Show the window
        cv2.waitKey(0)
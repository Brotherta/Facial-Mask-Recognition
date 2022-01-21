#!/usr/bin/env python
'''
Usage:
    ./detection_v2.py image_filepath
'''

import numpy as np
import cv2
import argparse
import sys
import cv2
from PIL import Image
from tensorflow import keras
import tensorflow as tf
from matplotlib import pyplot as plt

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    model = keras.models.load_model("../../models/model_epoch50.h5")
    net = cv2.dnn.readNetFromCaffe("face-detection/weights-prototxt.txt", "face-detection/res_ssd_300Dim.caffeModel")
    # load the input image by resizing to 300x300 dims
    image = cv2.imread(sys.argv[1])
    (height, width) = image.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0,
        (300, 300), (104.0, 177.0, 123.0))

    # pass the blob into the network
    net.setInput(blob)
    detections = net.forward()

    imOut = image.copy()

    # loop over the detections to extract specific confidence
    for i in range(0, detections.shape[2]):
            # extract the confidence (i.e., probability) associated with the
        # prediction
        confidence = detections[0, 0, i, 2]

        # greater than the minimum confidence
        if confidence > 0.5:
            box = detections[0, 0, i, 3:7] * np.array([width, height, width, height])
            (x1, y1, x2, y2) = box.astype("int")
            y = y1 - 10 if y1 - 10 > 10 else y1 + 10

            img = cv2.cvtColor(image[y1:y2,x1:x2], cv2.COLOR_BGR2RGB)
            img = cv2.resize(img, (120, 120))
            img = keras.preprocessing.image.img_to_array(img)
            img = tf.expand_dims(img, 0)  # Create batch axis
            predictions = model.predict(img)
            score = predictions[0]
            maskScore = 100 * (1 - score);
            nomaskScore = 100 * score;
            if maskScore >= 99.9:
                cv2.rectangle(imOut, (x1, y1), (x2, y2), (0, 255, 0), 1, cv2.LINE_AA)
                cv2.putText(imOut, "Mask with " + "{:.4f}%".format(float(maskScore)), (x1, y), cv2.LINE_AA, 0.45, (0, 255, 0), 2)
            else:
                cv2.rectangle(imOut, (x1, y1), (x2, y2), (0, 255, 0), 1, cv2.LINE_AA)
                cv2.putText(imOut, "No_Mask with " + "{:.4f}%".format(float(nomaskScore)), (x1, y), cv2.LINE_AA, 0.45, (0, 255, 0), 1)

# show the output image
cv2.imshow("Output", imOut)
cv2.waitKey(0)
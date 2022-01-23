from tensorflow import keras
from tensorflow.keras import layers
import tensorflow as tf
import json
from PIL import Image
import shutil
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


data_augmentation = keras.Sequential(
    [
        layers.RandomFlip("horizontal"),
        layers.RandomRotation(0.1)
    ]
)


class DataPreProcessing:
    ''' Cette classe est utilisée dans le processus de pré-traitement d'un jeu de donnée.
        Elle est utilisée, afin de préparer le jeu de donnée à la prédiction.
    '''

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
        ''' Permet de nettoyer le dossier images en les suprimants. '''

        shutil.rmtree('.images')
        os.mkdir('.images')

    def run(self) -> None:
        ''' Permet de lancer tous le processus de pré-traitement. '''
        self.cleanImages()
        self.crop_bounding_boxes()
        self.resize_moved_images()

    def findLabels(self):
        ''' Permet de lire le fichier d'annotations, et d'initialiser les labels disponibles. '''
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
        ''' Permet de récupérer les images des bounding box du fichier d'annotation.
            La méthode va sauvegarder les images créer dans le fichier data_path_box
        '''
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
        ''' Permet d'uniformiser le dataset, et de déplacer les images dans les bons sous dossier. '''

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
                        im.save(
                            f"{self.data_path_resized}{label}/{box}", "JPEG")

    def split_data(self, new_base=None):
        ''' Permet de séparer les données en jeu d'entraînement et de test. '''

        if new_base is not None:
            self.data_path_resized_base = new_base
        
        subs = os.listdir(self.data_path_resized_base)

        for sub in subs:
            images = os.listdir(self.data_path_resized_base+sub)
            for image in images:
                im = Image.open(self.data_path_resized_base+sub+"/"+image)
                if im.size > self.image_size:
                    im.thumbnail(self.image_size, Image.ANTIALIAS)
                    im.save(self.data_path_resized_base+sub+"/"+image)

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
        ''' Applique l'augmentation des données sur les images du jeu de donnée, en réalisant des rotation aléatoire sur l'image.
        '''
        self.train = self.train.map(
            lambda x, y: (data_augmentation(x, training=True), y))

        self.train = self.train.prefetch(buffer_size=32)
        self.test = self.test.prefetch(buffer_size=32)

        return self.train, self.test

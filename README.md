# Facial-Mask-Recognition

## Introduction

#### This is a GUI Application, written with Python and PyQT.
#### The purpose is to allow the user to create a project, import images, and assign categories to user-drawn rectangles zones of the images.
#### The user can create multiple projects and save wherever he wants.
#### We created this application in order to prepare data for machine learning purpose.

## Screenshots

![alt text](https://github.com/Brotherta/Facial-Mask-Recognition/blob/main/resources/screenshots/project_list_window.png)
![alt text](https://github.com/Brotherta/Facial-Mask-Recognition/blob/main/resources/screenshots/main%20window.png)
![alt text](https://github.com/Brotherta/Facial-Mask-Recognition/blob/main/resources/screenshots/editor%20window.png)

## Prequirements
Make sur to import modules with pip !
```
pip install -r requirement.txt
```

## How to use the classificator

#### Usage : 
```
usage: main_predictor.py [-h] [--mode MODE] [--path PATH] [--model MODEL]

Facial Mask Recognition script.

optional arguments:
  -h, --help     show this help message and exit
  --mode MODE    Launch the script with the given option. Options: [train, predict, preprocess]
  --path PATH    The path of the input file/directory, needed for preprocess and predict mode. For the training mode,
                 if --path is not specified, it will take the folder resized_images/ by default.
  --model MODEL  The path of the model you want for train. By default the model 'final_model.h5' is loaded.
```

#### Examples : 

```
python main_predictor.py --mode predict --path my_image.png
```
Result :
![maskdetect](https://user-images.githubusercontent.com/1645347/150678301-5bd2e35f-704b-4b3c-84c0-add8441a9d0e.png)


## How to use the annotator

#### 0 - Run the program :
```
python app.py
```

#### 1 - Create the project :
![alt text](https://github.com/Brotherta/Facial-Mask-Recognition/blob/main/resources/screenshots/create%20project.png)

#### 2 - Open the project
![alt text](https://github.com/Brotherta/Facial-Mask-Recognition/blob/main/resources/screenshots/open%20project.png)

#### 3 - Import images
![alt text](https://github.com/Brotherta/Facial-Mask-Recognition/blob/main/resources/screenshots/import%20images.png)
![alt text](https://github.com/Brotherta/Facial-Mask-Recognition/blob/main/resources/screenshots/import%20images%202.png)

#### 4 - Create new labels
![alt text](https://github.com/Brotherta/Facial-Mask-Recognition/blob/main/resources/screenshots/create%20label.png)
![alt text](https://github.com/Brotherta/Facial-Mask-Recognition/blob/main/resources/screenshots/create%20label%202.png)

#### 5 - Open an image
![alt text](https://github.com/Brotherta/Facial-Mask-Recognition/blob/main/resources/screenshots/open%20an%20image.png)

#### 6 - Draw a rectangle with the left mouse button
![alt text](https://github.com/Brotherta/Facial-Mask-Recognition/blob/main/resources/screenshots/draw%20rectangle.png)

#### 7 - Double click the rectangle and assign a label to it
![alt text](https://github.com/Brotherta/Facial-Mask-Recognition/blob/main/resources/screenshots/double%20click.png)

#### 8 - Validate
![alt text](https://github.com/Brotherta/Facial-Mask-Recognition/blob/main/resources/screenshots/validate.png)

#### 9 - Do not forget to save the project
![alt text](https://github.com/Brotherta/Facial-Mask-Recognition/blob/main/resources/screenshots/save.png)

#### 11 - The project folder looks like this :
![alt text](https://github.com/Brotherta/Facial-Mask-Recognition/blob/main/resources/screenshots/project%20folder.png)

#### 12 - That's all ! 

## Project files syntax

#### Project.ini
```
[PROJECT]
name = Masks
filepath = /Users/jipey/Desktop/masks
labels = /Users/jipey/Desktop/masks/labels.json
box = /Users/jipey/Desktop/masks/box.json
images = /Users/jipey/Desktop/masks/images
```

#### Box.json
```
[
    {
        "filepath": "/Users/jipey/Desktop/masks/images/image.jpg",
        "boxList": [
            {
                "x": 995,
                "y": 141,
                "width": 557,
                "height": 411,
                "label": {
                    "name": "white mask"
                }
            }
        ],
        "imageSize": [
            2048,
            1152
        ]
    },
    {
        "filepath": "/Users/jipey/Desktop/masks/images/mask1.jpg",
        "boxList": [
            {
                "x": 495,
                "y": 143,
                "width": 106,
                "height": 113,
                "label": {
                    "name": "blue mask"
                }
            },
            {
                "x": 813,
                "y": 169,
                "width": 87,
                "height": 89,
                "label": {
                    "name": "blue mask"
                }
            },
            {
                "x": 335,
                "y": 136,
                "width": 57,
                "height": 68,
                "label": {
                    "name": "blue mask"
                }
            },
            {
                "x": 181,
                "y": 128,
                "width": 63,
                "height": 68,
                "label": {
                    "name": "blue mask"
                }
            }
        ],
        "imageSize": [
            1024,
            682
        ]
    }
]
```

#### Labels.json
```
[
    {
        "name": "blue mask"
    },
    {
        "name": "white mask"
    }
]
```

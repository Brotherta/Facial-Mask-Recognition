# Facial-Mask-Recognition

## Introduction

#### This is a GUI Application, written with Python and PyQT.
#### The purpose is to allow the user to create a project, import images, and assign categories to user-drawn rectangles zones of the images.
#### The user can create multiple projects and save wherever he wants.
#### We created this application in order to prepare data for machine learning purpose.

## Screenshots

<img width="1012" alt="project_list_window" src="https://user-images.githubusercontent.com/1645347/150678415-17279756-0f10-4160-8231-815e9d957c5b.png">
<img width="1280" alt="main window" src="https://user-images.githubusercontent.com/1645347/150678427-0594d410-2583-4e10-b83c-fd1b2d349644.png">
<img width="1280" alt="editor window" src="https://user-images.githubusercontent.com/1645347/150678431-48f6ca4d-78fa-43f5-9cf2-d735e38e25bb.png">


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
<img width="904" alt="create project" src="https://user-images.githubusercontent.com/1645347/150678441-181b9ad7-ce77-4be1-9ded-ca46edf7ceb4.png">

#### 2 - Open the project
<img width="904" alt="open project" src="https://user-images.githubusercontent.com/1645347/150678451-383538fa-ce62-4057-adf0-1121fd605c93.png">

#### 3 - Import images
<img width="1280" alt="import images 2" src="https://user-images.githubusercontent.com/1645347/150678457-d23a90a2-82cd-4871-ace0-d93ce0b0825a.png">
<img width="1346" alt="import images" src="https://user-images.githubusercontent.com/1645347/150678459-89369beb-6b92-4a01-b0cd-051b75e80f97.png">


#### 4 - Create new labels
<img width="1280" alt="create label" src="https://user-images.githubusercontent.com/1645347/150678468-ffafc291-8ce0-41c8-876c-21f6f7ba1148.png">
<img width="512" alt="create label 2" src="https://user-images.githubusercontent.com/1645347/150678472-321db020-9bba-4956-8327-ce6ffb1b4567.png">

#### 5 - Open an image
<img width="1392" alt="open an image" src="https://user-images.githubusercontent.com/1645347/150678477-6fc64f65-3cf8-48b9-9613-0ea5c4757b56.png">

#### 6 - Draw a rectangle with the left mouse button
<img width="1072" alt="draw rectangle" src="https://user-images.githubusercontent.com/1645347/150678486-3cd1df91-4e96-41e2-86c1-a38cecd7c9cd.png">

#### 7 - Double click the rectangle and assign a label to it
<img width="1280" alt="double click" src="https://user-images.githubusercontent.com/1645347/150678491-51248418-ddf3-4a6f-b4fa-9f01dbfbad03.png">

#### 8 - Validate
<img width="1280" alt="validate" src="https://user-images.githubusercontent.com/1645347/150678497-32089fcc-9dea-4e7b-813c-02466abd311b.png">

#### 9 - Do not forget to save the project
<img width="1280" alt="save" src="https://user-images.githubusercontent.com/1645347/150678500-8c07bbdd-05d7-4ce7-b82b-12e6d1ae5946.png">

#### 11 - The project folder looks like this :
<img width="1032" alt="project folder" src="https://user-images.githubusercontent.com/1645347/150678504-9c3ef6fe-e2f8-466e-a54f-f4160101b52b.png">

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

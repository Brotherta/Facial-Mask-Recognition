#!/usr/bin/env python
'''
Usage:
    ./main_predictor.py  --mode [preprocess | train | predict] [--path INPUT_PATH] [--model MODEL_PATH]

    For help please see ./pipeline.py -h

'''

import argparse
from pre.DataPreProcessing import DataPreProcessing
from src.predictor.pipeline import Pipeline
import os

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='Facial Mask Recognition script.')
    parser.add_argument(
        "--mode", help="Launch the script with the given option. Options: [train, predict, preprocess]")
    parser.add_argument(
        "--path", help="The path of the input file/directory, needed for preprocess and predict mode")
    parser.add_argument(
        "--model", help="The path of the model you want for train. By default the model 'final_model.h5' is loaded.")
    args = parser.parse_args()

    if args.mode == "preprocess":
        if args.path:
            print("Launching preprocess mode with ", args.path, " file.")
            pre_processing = DataPreProcessing(
                annotationsJsonPath=args.path, image_size=(120, 120))
            pre_processing.run()

        else:
            print("Missing --path argument.")
            print(__doc__)

    elif args.mode == "train":

        print("Launching training mode...")
        if args.path and not os.path.isdir(args.path):
            args.path = None

        pre_processing = DataPreProcessing(
            image_size=(120, 120),
            batch_size=32,
        )

        pre_processing.split_data(args.path)
        data = pre_processing.increase_data()

        p = Pipeline(
            data=data,
            epochs=50
        )

        p.make_model()
        p.fit_model()

    elif args.mode == "predict":
        if args.path:
            print("preprocess mode with ", args.path)
            p = Pipeline()
            
            if args.model:
                p.load_model(args.model)
            else:
                p.load_model("./models/model_final.h5")

            p.predict_input_image(args.path)

        else:
            print("Missing --path argument.")
            print(__doc__)
    else:
        print(__doc__)

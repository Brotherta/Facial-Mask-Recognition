#!/usr/bin/env python
'''
Usage:
    ./pipeline.py  --mode [preprocess | train | predict] [--path INPUT_PATH]

'''

import argparse
from src.predictor.pipeline import DataPreProcessing
from src.predictor.pipeline import Pipeline


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='Facial Mask Recognition script.')
    parser.add_argument(
        "--mode", help="Launch the script with the given option.", required=True)
    parser.add_argument(
        "--path", help="The path of the input file/directory, needed for preprocess and predict mode")
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

        pre_processing = DataPreProcessing(
            image_size=(120, 120),
            batch_size=32
        )

        pre_processing.split_data()
        data = pre_processing.increase_data()

        p = Pipeline(
            data=data,
            epochs=50,
        )

        p.make_model()
        p.fit_model()

    elif args.mode == "predict":
        if args.path:
            print("preprocess mode with ", args.path)
            p = Pipeline()
            p.load_model("./models/model_final.h5")
            p.predict_input_image(args.path)

        else:
            print("Missing --path argument.")
            print(__doc__)
    else:
        print(__doc__)

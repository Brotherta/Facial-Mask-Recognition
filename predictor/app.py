#!/usr/bin/env python
'''
Usage:
    ./pipeline.py  --mode [preprocess | train | predict] [--path INPUT_PATH]

'''

import argparse



if __name__ == "__main__":
    # from src.pipeline import DataPreProcessing  
    # pre_processing = DataPreProcessing(annotationsJsonPath="", image_size=(120, 120))
    # pre_processing.resize_moved_images()


    parser = argparse.ArgumentParser(description='Facial Mask Recognition script.')
    parser.add_argument("--mode", help="Launch the script with the given option.", required=True)
    parser.add_argument("--path", help="The path of the input file/directory, needed for preprocess and predict mode")
    args = parser.parse_args()

    if args.mode == "preprocess":
        if args.path:
            from src.pipeline import DataPreProcessing
            print("Launching preprocess mode with ", args.path, " file.")

            pre_processing = DataPreProcessing(annotationsJsonPath=args.path, image_size=(120, 120))
            pre_processing.run()
        else:
            print("Missing --path argument.")
            print(__doc__)

    elif args.mode == "train":

        from src.pipeline import Pipeline
        from src.pipeline import DataPreProcessing
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
            size_entry_layers=[32, 64],
            size_block_layers=[128],
            size_exit_layers=256,
        )

        p.make_model3()
        p.fit_model()

        

    elif args.mode == "predict":
        if args.path:
            print("preprocess mode with ", args.path)
            print("Missing --path argument.")
            print(__doc__)
    else:
        print(__doc__)

    

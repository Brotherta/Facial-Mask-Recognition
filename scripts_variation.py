from src.predictor.pipeline import Pipeline
from src.predictor.pipeline import DataPreProcessing
from matplotlib import pyplot as plt
import json

if __name__ == "__main__":

    dp = DataPreProcessing(
        image_size=(120, 120),
        batch_size=32
    )
    dp.split_data()
    data = dp.increase_data()

    p = Pipeline(data=data, epochs=50)

    p.make_model()
    p.plot_model()
    p.fit_model()

    history = p.history

    with open(f"better.json", 'w') as fp:
        json.dump(history.history, fp, indent=4)

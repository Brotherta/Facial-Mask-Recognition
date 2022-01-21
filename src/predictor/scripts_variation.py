from glob import glob
from src.pipeline import Pipeline
from src.pipeline import DataPreProcessing

global epochs, input_shape, activation, size_block_layers, \
        size_entry_layers, size_exit_layers, dropout_layer, \
        dropout_rate, dense_activation, maxpooling_layer, NB_IT


def variating_dropout_rate():
    global dropout_rate, NB_IT

    dropout_rate = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6]


if __name__ == "__main__":
    pp = DataPreProcessing(
        image_size=(120, 120),
        batch_size=32
    )

    pp.resize_moved_images()
    pp.split_data()

    data = pp.increase_data()


    NB_IT = 5

    epochs = [5 for _ in range(NB_IT)]
    input_shape = [(120, 120) for _ in range(NB_IT)]
    activation = ["relu" for _ in range(NB_IT)]
    size_entry_layers = [[32, 64] for _ in range(NB_IT)]
    size_block_layers = [[128, 256, 512, 728] for _ in range(NB_IT)]
    size_exit_layers = [1024 for _ in range(NB_IT)]
    dropout_rate = [0.5 for _ in range(NB_IT)]
    dense_activation = ["sigmoid" for _ in range(NB_IT)]
    dropout_layer = [True for _ in range(NB_IT)]
    maxpooling_layer = [True for _ in range(NB_IT)]
    variating_dropout_rate()


    for i in range(NB_IT):
        print("New iteration with :",
            "\n epochs=", epochs[i],
            "\n input_shape=", input_shape[i],
            "\n activation=", activation[i],
            "\n size_entry_layers=", size_entry_layers[i],
            "\n size_block_layers=", size_block_layers[i],
            "\n size_exit_layers=", size_exit_layers[i],
            "\n dropout_rate=", dropout_rate[i],
            "\n dense_activation=", dense_activation[i],
            "\n dropout_layer=", dropout_layer[i],
            "\n maxpooling_layer=", maxpooling_layer[i]
        )
        p = Pipeline(
            data=data,
            epochs=epochs[i],
            input_shape=input_shape[i],
            activation=activation[i],
            size_entry_layers=size_entry_layers[i],
            size_block_layers=size_block_layers[i],
            size_exit_layers=size_exit_layers[i],
            dropout_rate=dropout_rate[i],
            dense_activation=dense_activation[i],
            dropout_layer=dropout_layer[i],
            maxpooling_layer=maxpooling_layer[i]
        )
        p.make_model()

        history = p.fit_model()

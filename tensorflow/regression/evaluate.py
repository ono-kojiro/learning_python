#!/usr/bin/env python3
# https://www.tensorflow.org/tutorials/keras/classification?hl=ja
import getopt
import sys
from pprint import pprint

import pandas as pd
import seaborn as sns

import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers


def norm(x, train_stats):
    return (x - train_stats["mean"]) / train_stats["std"]


def build_model(train_dataset):
    model = keras.Sequential(
        [
            layers.Dense(
                64, activation="relu", input_shape=[len(train_dataset.keys())]
            ),
            layers.Dense(64, activation="relu"),
            layers.Dense(1),
        ]
    )

    optimizer = tf.keras.optimizers.RMSprop(0.001)

    model.compile(loss="mse", optimizer=optimizer, metrics=["mae", "mse"])
    return model


class PrintDot(keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs):
        if epoch % 100 == 0:
            print("")
        print(".", end="")


EPOCHS = 1000


def plot_history(history):
    hist = pd.DataFrame(history.history)
    hist["epoch"] = history.epoch

    plt.figure()
    plt.xlabel("Epoch")
    plt.ylabel("Mean Abs Error [MPG]")
    plt.plot(hist["epoch"], hist["mae"], label="Train Error")
    plt.plot(hist["epoch"], hist["val_mae"], label="Val Error")
    plt.ylim([0, 5])
    plt.legend()

    plt.figure()
    plt.xlabel("Epoch")
    plt.ylabel("Mean Square Error [$MPG^2$]")
    plt.plot(hist["epoch"], hist["mse"], label="Train Error")
    plt.plot(hist["epoch"], hist["val_mse"], label="Val Error")
    plt.ylim([0, 20])
    plt.legend()
    # plt.show()
    plt.savefig("history.png")


def main():
    ret = 0

    model_path = None

    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "hvm:",
            [
                "version",
                "help",
                "model=",
            ],
        )
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(1)

    for o, a in opts:
        if o == "-v":
            usage()
            sys.exit(0)
        elif o in ("--help"):
            usage()
            sys.exit(0)
        elif o in ("--version"):
            usage()
            sys.exit(0)
        elif o in ("-o", "--output"):
            pass
        elif o in ("-m", "--model"):
            model_path = a

    # if output is None :
    # 	print('ERROR : no output option')
    # 	ret += 1

    if model_path is None:
        print("ERROR : no model option")
        ret += 1

    if ret != 0:
        sys.exit(1)

    dataset_path = keras.utils.get_file(
        "auto-mpg.data",
        "https://archive.ics.uci.edu/ml/machine-learning-databases/auto-mpg/auto-mpg.data",
    )

    column_names = [
        "MPG",
        "Cylinders",
        "Displacement",
        "Horsepower",
        "Weight",
        "Acceleration",
        "Model Year",
        "Origin",
    ]
    raw_dataset = pd.read_csv(
        dataset_path,
        names=column_names,
        na_values="?",
        comment="\t",
        sep=" ",
        skipinitialspace=True,
    )

    dataset = raw_dataset.copy()
    pprint(dataset.tail())

    pprint(dataset.isna().sum())

    dataset = dataset.dropna()

    origin = dataset.pop("Origin")

    dataset["USA"] = (origin == 1) * 1.0
    dataset["Europe"] = (origin == 2) * 1.0
    dataset["Japan"] = (origin == 3) * 1.0
    pprint(dataset.tail())

    train_dataset = dataset.sample(frac=0.8, random_state=0)
    test_dataset = dataset.drop(train_dataset.index)

    sns.pairplot(
        train_dataset[["MPG", "Cylinders", "Displacement", "Weight"]], diag_kind="kde"
    )

    # if train_dataset_png is not None :
    # 	print('INFO : savefig {0}'.format(train_dataset_png))
    # 	plt.savefig(train_dataset_png)

    train_stats = train_dataset.describe()
    train_stats.pop("MPG")
    train_stats = train_stats.transpose()
    pprint(train_stats)

    train_dataset.pop("MPG")
    test_labels = test_dataset.pop("MPG")

    norm(train_dataset, train_stats)
    normed_test_data = norm(test_dataset, train_stats)

    model = tf.keras.models.load_model(model_path)

    loss, mae, mse = model.evaluate(normed_test_data, test_labels, verbose=2)
    print(f"Testing set Mean Abs Error: {mae:5.2f} MPG")


if __name__ == "__main__":
    main()

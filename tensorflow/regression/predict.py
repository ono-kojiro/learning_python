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


def norm(x, train_stats):
    return (x - train_stats["mean"]) / train_stats["std"]


def main():
    ret = 0

    output = None
    model_path = None
    prediction_error_png = None

    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "hvm:o:e:",
            ["version", "help", "model=", "output=", "prediction-error="],
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
            output = a
        elif o in ("-e", "--prediction-error"):
            prediction_error_png = a
        elif o in ("-m", "--model"):
            model_path = a

    if output is None:
        print("ERROR : no output option")
        ret += 1

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

    # loss, mae, mse = model.evaluate(normed_test_data, test_labels, verbose=2)
    # print("Testing set Mean Abs Error: {:5.2f} MPG".format(mae))

    test_predictions = model.predict(normed_test_data).flatten()

    plt.figure()
    plt.scatter(test_labels, test_predictions)
    plt.xlabel("True Values [MPG]")
    plt.ylabel("Predictions [MPG]")
    plt.axis("equal")
    plt.axis("square")
    plt.xlim([0, plt.xlim()[1]])
    plt.ylim([0, plt.ylim()[1]])
    _ = plt.plot([-100, 100], [-100, 100])

    print(f"save {output}")
    plt.savefig(output)

    if prediction_error_png:
        plt.figure()
        error = test_predictions - test_labels
        plt.hist(error, bins=25)
        plt.xlabel("Prediction Error [MPG]")
        _ = plt.ylabel("Count")
        print(f"save {prediction_error_png}")
        plt.savefig(prediction_error_png)


if __name__ == "__main__":
    main()

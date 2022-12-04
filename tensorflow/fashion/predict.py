#!/usr/bin/env python3
import getopt
import sys
from pprint import pprint

import numpy as np
from PIL import Image

import tensorflow as tf
# https://www.tensorflow.org/tutorials/keras/classification?hl=ja


def main():
    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "hvo:n:",
            [
                "help",
                "version",
                "output=",
                "number=",
            ],
        )
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(1)


    if len(args) == 0:
        print("ERROR : no input images")
        sys.exit(1)

    model = tf.keras.models.load_model("models/my_model")

    class_names = [
        "T-shirt/top",
        "Trouser",
        "Pullover",
        "Dress",
        "Coat",
        "Sandal",
        "Shirt",
        "Sneaker",
        "Bag",
        "Ankle boot",
    ]

    for filepath in args:
        test_image = np.array(Image.open(filepath).convert("L"), dtype=np.uint8)
        test_image.reshape((28, 28))

        test_image = test_image / 255.0

        test_images = np.expand_dims(test_image, 0)

        predictions = model.predict(test_images)
        print(f"filepath : {filepath}")
        pprint(predictions[0])

        class_id = np.argmax(predictions[0])
        class_name = class_names[class_id]
        print(f"predict : {class_name} ({class_id})")


if __name__ == "__main__":
    main()

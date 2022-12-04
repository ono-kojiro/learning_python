#!/usr/bin/env python3
# https://www.tensorflow.org/tutorials/keras/classification?hl=ja
import os
from pprint import pprint

import tensorflow as tf

fashion_mnist = tf.keras.datasets.fashion_mnist

(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()
train_images, test_images = train_images / 255.0, test_images / 255.0

model = tf.keras.models.Sequential(
    [
        tf.keras.layers.Flatten(input_shape=(28, 28)),
        tf.keras.layers.Dense(128, activation="relu"),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(10),
    ]
)

predictions = model(train_images[:1]).numpy()

# pprint(predictions)

tf.nn.softmax(predictions).numpy()

loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
loss_fn(train_labels[:1], predictions).numpy()

model.compile(optimizer="adam", loss=loss_fn, metrics=["accuracy"])


# https://www.tensorflow.org/tutorials/keras/save_and_load?hl=ja

checkpoint_path = "checkpoints/cp.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)
# チェックポイントコールバックを作る
cp_callback = tf.keras.callbacks.ModelCheckpoint(
    checkpoint_path, save_weights_only=False, verbose=1
)

# save_weights_only=True,

model.fit(train_images, train_labels, epochs=5, callbacks=[cp_callback])

res = model.evaluate(test_images, test_labels, verbose=2)
pprint(res)

model.save("models/my_model")

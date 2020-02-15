# import numpy as np
# import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from matplotlib import pyplot as plt
# import positive libraries
from mnist_reader import load_mnist
from mnist_reader import read_mnsit_test
# import sys
import os

# print(sys.argv)

# load data
# print(os.listdir('./'))
data_path = './fashion_MNIST'
print(os.listdir(data_path))
train_datas, train_labels = load_mnist(data_path, 'train')
test_datas, test_labels = load_mnist(data_path, 't10k')
read_mnsit_test()

# LetNet

LetNet_5 = keras.Sequential([
    layers.Conv2D(input_shape=((x_shape[1], x_shape[2], x_shape[3])),
                  filters=6,
                  kernel_size=(5, 5),
                  strides=(1, 1),
                  padding='same',
                  activation='relu'),
    layers.MaxPool2D(pool_size=(2, 2), strides=(2, 2), padding='same'),
    layers.Conv2D(filters=16,
                  kernel_size=(5, 5),
                  strides=(1, 1),
                  padding='valid',
                  activation='relu'),
    layers.MaxPool2D(pool_size=(2, 2), strides=(2, 2), padding='same'),
    layers.Conv2D(filters=120,
                  kernel_size=(5, 5),
                  strides=(1, 1),
                  padding='valid',
                  activation='relu'),
    layers.MaxPool2D(pool_size=(2, 2), strides=(2, 2), padding='same'),
    layers.Flatten(),
    layers.Dense(84, activation='relu'),
    layers.Dense(10, activation='softmax')
])

LetNet_5.compile(optimizer=keras.optimizers.Adam(),
                 loss=keras.losses.SparseCategoricalCrossentropy(),
                 metrics=['accuracy'])
LetNet_5.summary()  # 打印网络结构

# training

history = LetNet_5.fit(train_datas,
                       train_labels,
                       batch_size=64,
                       epochs=5,
                       validation_split=0.1)

plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.legend(['training', 'valivation'], loc='upper left')
plt.show()

res = LetNet_5.evaluate(test_datas, test_labels)

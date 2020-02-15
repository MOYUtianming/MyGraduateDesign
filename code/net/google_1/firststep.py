from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

# Helper Libraries
import matplotlib.pyplot as plt
import numpy as np
# Tensorflow and Keras
import tensorflow as tf
from tensorflow import keras

# 0. print tensorflow version
print(tf.__version__)

# 1.0 load dataset_fashion_MNIST
# 1.1 load dataset
fashion_mnist = keras.datasets.fashion_mnist
((train_images, train_labels), (test_images,
                                test_labels)) = fashion_mnist.load_data()

# 1.2 set data's labels
class_names = [
    'T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 'Sandal', 'Shirt',
    'Sneaker', 'Bag', 'Ankle boot'
]
# 2.0 Simple test dataset
# 2.1 show the shape of this dataset
'''
    print(train_images.shape)
    print(len(train_labels))
    print(test_images.shape)
    print(len(test_labels))
    print(train_labels)
'''

# 2.2 show the first image
'''
    plt.figure()
    plt.imshow(train_images[0])
    plt.colorbar()
    plt.grid(False)
    plt.show()
'''
# 3.0 Preprocess dataset from 0~255 to 0~1
train_images = train_images / 255.0
test_images = test_images / 255.0

# 3.1 Show the first 25 images with their labels to verify the data format
'''
    plt.figure(figsize=(10, 10))
    for i in range(25):
        plt.subplot(5, 5, i + 1)
        plt.xticks([])
        plt.yticks([])
        plt.grid(False)
        plt.imshow(train_images[i], cmap=plt.cm.binary)
        plt.xlabel(class_names[train_labels[i]])
    plt.show()
'''
# 4.0 build the model
# 4.1 Set up layers
model = keras.Sequential([
    # flatten layer transform the format of the images from
    # a two-dimensional array(of 28 by 28 pixel)
    # to a one-dimensional array(of 28*28=784 pixels)
    keras.layers.Flatten(input_shape=(28, 28)),
    # two fully connected layers
    # the first layer has 128 nodes
    # the second and last layer is a softmax layer include 10 nodes
    # ( or neurons)
    # it return an array of 10 probability scores that sums to 1
    # each node contains a score that indicates the probability
    # that the current image belongs to one of the 10 classes
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(10)
])
# 4.2 Compile the model
# Three elements are needed to set
# 01 Loss Function--measures how accurate the model is during learning
#                   we should minimize the parameter to steer the model
#                   in the right direction
# 02 Optimizer--set how the model is updated based on the data it sees
#               and it's loss function
# 03 Metrics--used to monitor the training and testing steps
model.compile(
    optimizer='adam',
    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    metrics=['accuracy'])

# 5.0 Train the model
# 5.1 Feed the model with training data ,
#     in this example , they are train_images and train_labels.
#     and the model learn to associate images and labels
model.fit(train_images, train_labels, epochs=10)

# 5.2 Evaluate accuracy
#     to verify the result by test the lossdata and accuracydata
test_loss, test_acc = model.evaluate(test_images, test_labels, verbose=2)
# if the test_acc is less than 1 , it means the model
# behave worse on the test_data than on the training_data,
# in other word, it means overfitting.
# Overfitting is when a machine learning model performs worse on
# new, previously unseen inputs than on the training data.

# 5.3 Make predictions
# 01 transform the model's linear output(logits) to be probabilities,
#    which are easier to interpret.
probability_model = tf.keras.Sequential([model, tf.keras.layers.Softmax()])
# 02 predict labels for each images in test_images set
predictions = probability_model.predict(test_images)
# 03 Take a look at the first prediction
predictions[0]
#    and we can see which label has the highest confidence value
#    in this sample;
np.argmax(predictions[0])
#    we can print the corresponding label to test
#    if the prediction is correct or not.
test_labels[0]

# 5.4 Verify predictions


def plot_image(i, predictions_array, true_label, img):
    predictions_array, true_label, img = predictions_array, true_label[i], img[
        i]
    plt.grid(False)
    plt.xticks([])
    plt.yticks([])
    plt.imshow(img, cmap=plt.cm.binary)
    predicted_label = np.argmax(predictions_array)
    if predicted_label == true_label:
        color = 'blue'
    else:
        color = 'red'

    plt.xlabel("{} {:2.0f}% ({})".format(class_names[predicted_label],
                                         100 * np.max(predictions_array),
                                         class_names[true_label]),
               color=color)


def plot_value_array(i, predictions_array, true_label):
    predictions_array, true_label = predictions_array, true_label[i]
    plt.grid(False)
    plt.xticks(range(10))
    plt.yticks([])
    thisplot = plt.bar(range(10), predictions_array, color="#777777")
    plt.ylim([0, 1])
    predicted_label = np.argmax(predictions_array)

    thisplot[predicted_label].set_color('red')
    thisplot[true_label].set_color('blue')


# 01 plot one correct example and one error example
#    correct one
i = 0
plt.figure(figsize=(6, 3))
plt.subplot(1, 2, 1)
plot_image(i, predictions[i], test_labels, test_images)
plt.subplot(1, 2, 2)
plot_value_array(i, predictions[i], test_labels)
plt.show()
#    error one
i = 12
plt.figure(figsize=(6, 3))
plt.subplot(1, 2, 1)
plot_image(i, predictions[i], test_labels, test_images)
plt.subplot(1, 2, 2)
plot_value_array(i, predictions[i], test_labels)
plt.show()

# 02 Plot the first 5X3 test images, their predicted labels, and
#    the true labels.
#    Color correct predictions in blue and incorrect predictions in red.
num_rows = 5
num_cols = 3
num_images = num_rows * num_cols
plt.figure(figsize=(2 * 2 * num_cols, 2 * num_rows))
for i in range(num_images):
    plt.subplot(num_rows, 2 * num_cols, 2 * i + 1)
    plot_image(i, predictions[i], test_labels, test_images)
    plt.subplot(num_rows, 2 * num_cols, 2 * i + 2)
    plot_value_array(i, predictions[i], test_labels)
plt.tight_layout()
plt.show()

# 6 Use the model
# 6.1 Grab an image from the test dataset.
img = test_images[1]

print(img.shape)

# 6.2 Add the image to a batch where it's the only member.
img = (np.expand_dims(img, 0))

print(img.shape)
# 6.3 predict the correct label and print them
predictions_single = probability_model.predict(img)

print(predictions_single)
# 6.4 print the answer.
print(np.argmax(predictions_single[0]))
# 6.5 plot the 10 probabilities
plot_value_array(1, predictions_single[0], test_labels)
_ = plt.xticks(range(10), class_names, rotation=45)
plt.show()

print('end')

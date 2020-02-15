# error
probability_model = tf.keras.Sequential([model, tf.keras.layers.softmax()])

# right
probability_model = tf.keras.Sequential([model, tf.keras.layers.Softmax()])


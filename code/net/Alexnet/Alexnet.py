import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
def AlexNet_inference(in_shape):
    model = keras.Sequential(name='AlexNet')  
 
    # model.add(layers.Conv2D(96,(11,11),strides=(4,4),input_shape=(in_shape[1],in_shape[2],in_shape[3]),
                # padding='same',activation='relu',kernel_initializer='uniform')) 
                
    model.add(layers.Conv2D(96,(11,11),strides=(2,2),input_shape=(in_shape[1],in_shape[2],in_shape[3]),
                padding='same',activation='relu',kernel_initializer='uniform'))  
    model.add(layers.MaxPooling2D(pool_size=(3,3),strides=(2,2)))  
    model.add(layers.Conv2D(256,(5,5),strides=(1,1),padding='same',activation='relu',kernel_initializer='uniform'))  
    model.add(layers.MaxPooling2D(pool_size=(3,3),strides=(2,2)))  
    model.add(layers.Conv2D(384,(3,3),strides=(1,1),padding='same',activation='relu',kernel_initializer='uniform'))  
    model.add(layers.Conv2D(384,(3,3),strides=(1,1),padding='same',activation='relu',kernel_initializer='uniform'))  
    model.add(layers.Conv2D(256,(3,3),strides=(1,1),padding='same',activation='relu',kernel_initializer='uniform'))  
    model.add(layers.MaxPooling2D(pool_size=(2,2),strides=(2,2)))  
    model.add(layers.Flatten())  
    model.add(layers.Dense(2048,activation='relu'))  
    model.add(layers.Dropout(0.5))  
    model.add(layers.Dense(2048,activation='relu'))  
    model.add(layers.Dropout(0.5))  
    model.add(layers.Dense(10,activation='softmax'))  
    model.compile(optimizer=keras.optimizers.Adam(),
                loss='sparse_categorical_crossentropy', #不能直接用函数，否则在与测试加载模型不成功！
                metrics=['accuracy'])
    model.summary()  
 
    return model


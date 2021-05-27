# -*- coding: utf-8 -*-
"""
@author: www.erdemece.net
"""

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Dropout, Flatten 
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import load_model

import data_preprocessing 

x_train=data_preprocessing.x_train
y_train=data_preprocessing.y_train

print()
input_shape= (75,100,3)
num_classes =7 
epochs=10
batch_size=16

#initialize model

model=Sequential()
model.add(Conv2D(32,kernel_size=(3,3),activation="relu",padding="same",input_shape=input_shape))
model.add(Conv2D(32,kernel_size=(3,3),activation="relu",padding="same"))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.25))

model.add(Conv2D(32,kernel_size=(3,3),activation="relu",padding="same"))
model.add(Conv2D(32,kernel_size=(3,3),activation="relu",padding="same"))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.25))

model.add(Flatten())

model.add(Dense(128,activation="relu"))
model.add(Dropout(0.25))
model.add(Dense(num_classes,activation="softmax")) #more than 1 class
model.summary()


optimizers = Adam(lr=0.001)
model.compile(optimizer=optimizers, loss="categorical_crossentropy",metrics=["accuracy"])

model_history=model.fit(x=x_train, y=y_train, batch_size=batch_size, epochs=epochs , verbose=1, shuffle= True)

model.save("skin_cancer.h5")
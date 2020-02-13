import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.applications import ResNet50V2

class NN():

  def __init__(self):
    self.resnet = ResNet50V2(include_top=False, pooling='avg')
    self.model = keras.Sequential()
    self.model.add(self.resnet)
    self.model.add(keras.layers.Dense(1))

    self.model.layers[0].trainable = False
      
  def get_compile_model(self):
    self.model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])

    return self.model

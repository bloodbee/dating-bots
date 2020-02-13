import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.applications import ResNet50V2

import os
import cv2
import dlib
import os.path
import numpy as np

MODEL_PATH = './face_detector/face_detector.dat'

RESNET_MODEL_PATH = './model/beauty_nn.h5'

class NN():

  def __init__(self):
    self.resnet = ResNet50V2(include_top=False, pooling='avg')
    self.model = keras.Sequential()
    self.model.add(self.resnet)
    self.model.add(keras.layers.Dense(1))

    self.model.layers[0].trainable = False

    self.cnn_face_detector = dlib.cnn_face_detection_model_v1(MODEL_PATH)
      
  def get_compile_model(self):
    self.model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])

    return self.model

  def get_model(self):
    return self.model

  def save(self):
    self.model.save(RESNET_MODEL_PATH)

  def load(self):
    self.model.load_weights(RESNET_MODEL_PATH)

  def score_mapping(self, modelScore):
    mappingScore = 0
    if modelScore <= 3.4:
      mappingScore = 5/3 * modelScore + 5/6
    elif modelScore <= 4:
      mappingScore = 5/2 * modelScore - 2
    elif modelScore < 5:
      mappingScore = modelScore + 4

    return mappingScore

  def scores(self, path):
    im0 = cv2.imread(os.path.join(path))

    if im0.shape[0] > 1280:
      new_shape = (1280, im0.shape[1] * 1280 / im0.shape[0])
    elif im0.shape[1] > 1280:
      new_shape = (im0.shape[0] * 1280 / im0.shape[1], 1280)
    elif im0.shape[0] < 640 or im0.shape[1] < 640:
      new_shape = (im0.shape[0] * 2, im0.shape[1] * 2)
    else:
      new_shape = im0.shape[0:2]

    im = cv2.resize(im0, (int(new_shape[1]), int(new_shape[0])))
    dets = self.cnn_face_detector(im, 0)

    ret = []
    for i, d in enumerate(dets):
      face = [d.rect.left(), d.rect.top(), d.rect.right(), d.rect.bottom()]
      face[0] = max(0, face[1])
      face[1] = max(0, face[1])
      face[2] = min(im.shape[1] - 1, face[2])
      face[3] = min(im.shape[0] - 1, face[3])
      croped_im = im[face[1]:face[3], face[0]:face[2], :]
      try:
        resized_im = cv2.resize(croped_im, (224, 224))
      except:
        break
      normed_im = np.array([(resized_im - 127.5) / 127.5])

      pred = self.model.predict(normed_im)
      ldList = pred[0]
      out = (1 * ldList[0] + 2 * ldList[1] + 3 * ldList[2] + 4 * ldList[3] + 5 * ldList[4])
      ret.append(score_mapping(out))
    return ret

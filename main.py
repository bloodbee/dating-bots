from __future__ import absolute_import, division, print_function, unicode_literals
import sys, os
from tinder_bot import TinderBot
from resnet50 import NN

import numpy
import cv2
from sklearn.model_selection import train_test_split

gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
  # Restrict TensorFlow to only use the first GPU
  try:
    tf.config.experimental.set_visible_devices(gpus[0], 'GPU')
    logical_gpus = tf.config.experimental.list_logical_devices('GPU')
    print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPU")
  except RuntimeError as e:
    # Visible devices must be set before GPUs have been initialized
    print(e)

def main(argv):
  """
  Main function to manage commands and what to do.
  """
  if '-h' in sys.argv: # display help
    print('main.py -l || main.py -m || main.py -t')
    print('-l will launch the bot and start the auto swipe')
    print('-m will launch the bot and message all matched persons')
    print('-t will train the model against the facial dataset')
    print('One bot at a time !')
    sys.exit()
  elif '-l' in sys.argv: # launch auto swipe
    print('Launch the bot in auto swipe mode...')
    bot = TinderBot()
    bot.login()
    bot.auto_swipe()
    bot.quit()
  elif '-m' in sys.argv: # launch message all
    print('Launch the bot in message all matchs mode...')
    bot = TinderBot()
    bot.login()
    bot.message_all()
    bot.quit()
  elif '-t' in sys.argv: # launch neural network training
    nn = NN()
    model = nn.get_compile_model()

    print(model.summary())

    # open the labels
    full_images = []
    full_scores = []

    with open('dataset/train_test_files/All_labels.txt', 'r') as f:
      # read line
      lines = f.readlines()

      for line in lines:
        # split img label and scoring label
        labels = line.split(' ')

        # open the image with cv2
        im = cv2.imread('dataset/Images/{}'.format(labels[0]))

        full_images.append(im)
        full_scores.append(float(labels[1]))

    # split dataset
    train_images, test_images, train_labels, test_labels = train_test_split(full_images, full_scores, test_size=0.20)

    # fit
    model.fit(batch_size=32, x=numpy.array(train_images), y=numpy.array(train_labels), epochs=100)

    # check accuracy
    results = model.evaluate(numpy.array(test_images), numpy.array(test_labels))
    for value in results:
      print('loss', ' : ', value[0])
      print('accuracy', ' : ', value[1])

    # save model
    model.save('beauty_nn.h5')
      

if __name__ == "__main__":
  main(sys.argv[1:])
  exit()
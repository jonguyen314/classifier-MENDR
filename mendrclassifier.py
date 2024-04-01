# -*- coding: utf-8 -*-
"""mendrv1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1PAmlHZshROIBWPlT_gN5Eb4_pS7gX63W
"""

import os
import zipfile
import random
import shutil
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from shutil import copyfile
import matplotlib.pyplot as plt

! rm -rf forML.zip
! rm -rf "/forML"

local_zip = '/forML.zip'
zip_ref   = zipfile.ZipFile(local_zip, 'r')
zip_ref.extractall('/forML')
zip_ref.close()

source_path = '/forML/forML'

train_hit_path = "/forML/forML/training/hit"
train_nothit_path = "/forML/forML/training/nothit"
test_hit_path="/forML/forML/testing/hit"
test_nothit_path="/forML/forML/testing/nothit"


# os.listdir returns a list containing all files under the given path
print(f"There are {len(os.listdir(train_hit_path))} images of hits to train.")
print(f"There are {len(os.listdir(train_nothit_path))} images of not-a-hit to train.")
print(f"There are {len(os.listdir(test_hit_path))} images of hits to test.")
print(f"There are {len(os.listdir(test_nothit_path))} images of not-a-hit to test.")

def train_val_generators(TRAINING_DIR, VALIDATION_DIR):
  ### START CODE HERE

  # Instantiate the ImageDataGenerator class (don't forget to set the arguments to augment the images)
  train_datagen = ImageDataGenerator(rescale=1./255,
                                     rotation_range=.2,
                                     shear_range=0,
                                     zoom_range=.2,
                                     brightness_range=[0.2, 1],
                                     horizontal_flip=True,
                                     fill_mode="reflect")

  # Pass in the appropriate arguments to the flow_from_directory method
  train_generator = train_datagen.flow_from_directory(directory=TRAINING_DIR,
                                                      batch_size=10,
                                                      class_mode='binary',
                                                      target_size=(150, 150))

  # Instantiate the ImageDataGenerator class (don't forget to set the rescale argument)
  validation_datagen = ImageDataGenerator( rescale = 1.0/255. )

  # Pass in the appropriate arguments to the flow_from_directory method
  validation_generator = validation_datagen.flow_from_directory(directory=VALIDATION_DIR,
                                                                batch_size=5,
                                                                class_mode='binary',
                                                                target_size=(150, 150))
  ### END CODE HERE
  return train_generator, validation_generator

TRAINING_DIR="/forML/forML/training"
VALIDATION_DIR="/forML/forML/testing"
train_generator, validation_generator = train_val_generators(TRAINING_DIR, VALIDATION_DIR)

def create_model():
  # DEFINE A KERAS MODEL TO CLASSIFY CATS V DOGS
  # USE AT LEAST 3 CONVOLUTION LAYERS

  ### START CODE HERE

  model = tf.keras.models.Sequential([

    tf.keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(150, 150,3)),
    #tf.keras.layers.BatchNormalization(),
    tf.keras.layers.MaxPooling2D(2,2),
    #tf.keras.layers.Dropout(0.25),

    # Flatten the results to feed into a DNN
    tf.keras.layers.Flatten(),
    # 512 neuron hidden layer
    tf.keras.layers.Dense(128, activation='relu'),
    # Only 1 output neuron. It will contain a value from 0-1 where 0 for 1 class ('hit') and 1 for the other ('not a hit')
    tf.keras.layers.Dense(1, activation='sigmoid')
  ])



  model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
                loss='binary_crossentropy',
                metrics=['accuracy'])

  ### END CODE HERE

  return model

# Get the untrained model
model = create_model()

# Train the model
history = model.fit(train_generator,
                    epochs=15,
                    verbose=1,
                    validation_data=validation_generator)

#-----------------------------------------------------------
# Retrieve a list of list results on training and test data
# sets for each training epoch
#-----------------------------------------------------------
acc=history.history['accuracy']
val_acc=history.history['val_accuracy']
loss=history.history['loss']
val_loss=history.history['val_loss']

epochs=range(len(acc)) # Get number of epochs

#------------------------------------------------
# Plot training and validation accuracy per epoch
#------------------------------------------------
plt.plot(epochs, acc, 'r', "Training Accuracy")
plt.plot(epochs, val_acc, 'b', "Validation Accuracy")
plt.title('Training and validation accuracy')
plt.show()
print("")

#------------------------------------------------
# Plot training and validation loss per epoch
#------------------------------------------------
plt.plot(epochs, loss, 'r', "Training Loss")
plt.plot(epochs, val_loss, 'b', "Validation Loss")
plt.show()

import numpy as np
from google.colab import files
from keras.preprocessing import image

uploaded = files.upload()

for fn in uploaded.keys():

  # predicting images
  path = '/content/' + fn
  img = image.load_img(path, target_size=(150, 150))
  x = image.img_to_array(img)
  x /= 255
  x = np.expand_dims(x, axis=0)

  images = np.vstack([x])
  classes = model.predict(images, batch_size=1)
  print(classes[0])
  if classes[0]>0.5:
    print(fn + " is not a hit")
  else:
    print(fn + " is a hit")
from __future__ import print_function

import os
from math import ceil

import keras
from keras.datasets import cifar10
from keras.layers import (Activation, Conv2D, Dense, Dropout, Flatten,
                          MaxPooling2D)
from keras.models import Sequential
from keras.preprocessing.image import ImageDataGenerator

BATCH_SIZE = 32
NUM_CLASSES = 10
EPOCHS = 100
AUGMENTATION = True

SAVE_DIR = os.path.join(os.getcwd(), 'model_weights')
MODEL_NAME = 'docker_cifar10_model.h5'

def create_folders(path):
    if not os.path.exists(path):
        os.makedirs(path)

def initialize_dataset():
    (x_train, y_train), (x_test, y_test) = cifar10.load_data()
    print('x_train shape:', x_train.shape)
    print(x_train.shape[0], 'train samples')
    print(x_test.shape[0], 'test samples')
    return x_train, y_train, x_test, y_test


def converting_the_labels(y_train, y_test):
    y_train = keras.utils.to_categorical(y_train, NUM_CLASSES)
    y_test = keras.utils.to_categorical(y_test, NUM_CLASSES)
    return y_train, y_test

def scaling_the_data(x_train, x_test):
    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')
    x_train /= 255
    x_test /= 255
    return x_train, x_test

def define_cnn_model(image_shape):
    model = Sequential()
    model.add(Conv2D(32, (3, 3), padding='same',
                    input_shape=image_shape))
    model.add(Activation('relu'))
    model.add(Conv2D(32, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Conv2D(64, (3, 3), padding='same'))
    model.add(Activation('relu'))
    model.add(Conv2D(64, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(NUM_CLASSES))
    model.add(Activation('softmax'))

    return model


def generating_augmentation(x_train):
    datagen = ImageDataGenerator(
        featurewise_center=False,  
        samplewise_center=False, 
        featurewise_std_normalization=False, 
        samplewise_std_normalization=False,
        zca_whitening=False,
        zca_epsilon=1e-06,
        rotation_range=0,
        width_shift_range=0.1,
        height_shift_range=0.1,
        shear_range=0.,
        zoom_range=0., 
        channel_shift_range=0.,
        fill_mode='nearest',
        cval=0.,
        horizontal_flip=True,
        vertical_flip=False, 
        rescale=None,
        preprocessing_function=None,
        data_format=None,
        validation_split=0.0)

    datagen.fit(x_train)
    return datagen


def save_model(model):
    model_path = os.path.join(SAVE_DIR, MODEL_NAME)
    model.save(model_path)
    print('Saved trained model at %s ' % model_path)


def evaluate_model(model):
    scores = model.evaluate(x_test, y_test, verbose=1)
    print('Test loss:', scores[0])
    print('Test accuracy:', scores[1])


if __name__ == "__main__":
    
    x_train, y_train, x_test, y_test = initialize_dataset()
    y_train, y_test = converting_the_labels(y_train, y_test)
    x_train, x_test = scaling_the_data(x_train, x_test)
    image_shape = x_train.shape[1:]
    model = define_cnn_model(image_shape)
    opt = keras.optimizers.RMSprop(lr=0.0001, decay=1e-6)
    model.compile(loss='categorical_crossentropy',
              optimizer=opt,
              metrics=['accuracy'])

    steps_per_epoch = ceil(x_train.shape[0] / (BATCH_SIZE * 4))

    if AUGMENTATION:
        print('Using real-time data augmentation.')
        datagen = generating_augmentation(x_train)
        model.fit_generator(datagen.flow(x_train, y_train,
                                        batch_size=BATCH_SIZE),
                            epochs=EPOCHS,
                            validation_data=(x_test, y_test),
                            workers=4,
                            steps_per_epoch=steps_per_epoch)

    else:
        print('Not using data augmentation.')
        model.fit(x_train, y_train,
                batch_size=BATCH_SIZE,
                epochs=EPOCHS,
                validation_data=(x_test, y_test),
                shuffle=True)
    
    create_folders(SAVE_DIR)

    save_model(model)
    evaluate_model(model)

import keras
import numpy as np
import tensorflow as tf
import cv2
from keras.models import load_model
from keras.applications.vgg19 import VGG19
from keras.applications.vgg19 import decode_predictions


def image_prediction(image):
    MODEL = VGG19()

    image = cv2.imread(image)
    image = cv2.resize(image, (224, 224))
    image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
    
    yhat = MODEL.predict(image)
    label = decode_predictions(yhat)
    label = label[0][0]
    label, conf = label[1], label[2]*100
    return label, conf
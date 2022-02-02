import numpy as np

import cv2
import keras
import tensorflow as tf
from keras.applications.vgg19 import VGG19, decode_predictions
from keras.models import load_model


def image_prediction(image):
    MODEL = VGG19()
    try:
        image = cv2.imread(image)
        image = cv2.resize(image, (224, 224))
        image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
        
        yhat = MODEL.predict(image)
        label = decode_predictions(yhat)
        label = label[0][0]
        label, conf = label[1], label[2]*100
        results = [label, conf]

    except Exception as e:
        results = "Please check the image."
        
    return results

import json
# sys.path.append('/home/techject/Abhishek/C3-python/')
import os
import random
import sys
import time

import flask
from flask import render_template
from werkzeug import secure_filename

import cv2
import keras
import tensorflow as tf
from classifier import app
from classifier.backend.prediction import image_prediction


@app.route("/fetchingImage", methods = ['POST'])
def fetchingImage():
    if flask.request.method == 'POST':
        keras.backend.clear_session()
        image = flask.request.files['image']
        image.save(app.config['UPLOAD_FOLDER'] + secure_filename(image.filename))
        full_img = app.config['UPLOAD_FOLDER'] + image.filename
        data = image_prediction(full_img)
        if len(data)==2:
            return render_template('prediction.html', results = data)
        else:
            return render_template('error.html', results = data)

@app.route('/home')
def home():
    return render_template('home.html')

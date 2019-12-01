from classifier import app
import json
import sys
# sys.path.append('/home/techject/Abhishek/C3-python/')
import os
import urllib
import numpy as np
from werkzeug import secure_filename
import flask
import time
import cv2
import random
from flask import render_template
from classifier.backend.prediction import image_prediction


@app.route("/fetchingImage", methods = ['POST'])
def fetchingImage():
    if flask.request.method == 'POST':
        image = flask.request.files['image']
        image.save(app.config['UPLOAD_FOLDER'] + secure_filename(image.filename))
        img = cv2.imread(app.config['UPLOAD_FOLDER'] + image.filename)
        image_prediction(image)

        return "Success!!"


@app.route('/testing')
def testing():
    return render_template('home.html')

from searchapp import app
import json
import sys
# sys.path.append('/home/techject/Abhishek/C3-python/')
import os
from werkzeug import secure_filename
import flask
import time
import cv2
import random
import keras
import tensorflow as tf
from flask import render_template
from searchapp.backend.handle_requests import isLabelInDb

@app.route("/createLabels", methods = ['POST'])
def createLabels():
    if flask.request.method == 'POST':
        image = flask.request.files['image']
        label = flask.request.form['label']
        image.save(app.config['UPLOAD_FOLDER'] + secure_filename(image.filename))
        full_path = app.config['UPLOAD_FOLDER'] + image.filename

        alreadyPresent = isLabelInDb(label, full_path)            
        
        if alreadyPresent:
            '''
            Render the message that the label is already present. Try it with other label
            '''
        else:
            '''
            Render the message for successfully insertion of the image and label to db
            '''
            return render_template('prediction.html', results = data)

@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/fetchImages', methods=['GET'])
def fetchImages():
    if flask.request.method == 'POST':
        label = flask.request.form['label']
        
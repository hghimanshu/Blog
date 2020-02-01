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


@app.route("/createLabels", methods = ['POST'])
def fetchingImage():
    if flask.request.method == 'POST':
        image = flask.request.files['image']
        label = flask.request.form['label']

@app.route('/home')
def home():
    return render_template('home.html')

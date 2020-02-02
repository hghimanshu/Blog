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
from flask import render_template, url_for
from searchapp.backend.handle_requests import (isLabelInDb, 
                                            getRequiredImages, getAllImages,
                                            updateInfo)


@app.route("/createLabels", methods=['GET', 'POST'])
def createLabels():
    if flask.request.method == 'POST':
        image = flask.request.files['image']
        label = flask.request.form['label']
        image.save(app.config['UPLOAD_FOLDER'] + secure_filename(image.filename))
        full_path = app.config['UPLOAD_FOLDER'] + image.filename

        alreadyPresent = isLabelInDb(label, full_path)   
        
        if alreadyPresent:
            message = "The label is already in the database. Try with other label"
            return render_template('error.html', message = message)
        else:
            message = "The label is successfully inserted to the database"
            return render_template('success.html', message = message)
    else:
        return render_template('createLabels.html')

@app.route('/home')
def home():
    allImages = getAllImages()
    data = {}
    if len(list(allImages._CommandCursor__data)) != 0:
        for r in allImages:
            label = r['_id']
            images = r['image_path']
            data[label] = images
    return render_template('home.html', results=data)


@app.route('/fetchImages', methods=['POST'])
def fetchImages():
    if flask.request.method == 'POST':
        label = flask.request.form['label']
        totalImages = getRequiredImages(label)
        if len(totalImages) == 0:
            message = "No image is present in the database with the label " + str(label)
            return render_template('error.html', message = message)
        else:
            data = [totalImages, label]
            return render_template('show_images.html', results=data)


@app.route('/updateLabel', methods=['POST'])
def updateLabel():
    if flask.request.method == 'POST':
        print(flask.request.form)
        image = flask.request.form['image']
        curr_value = flask.request.form['current_label']
        new_value = flask.request.form['new_label']

        updateInfo(image, curr_value, new_value)
        message = "Label is updated !!"

        return render_template('success.html', message=message)
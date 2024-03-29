import json
import os

import flask
from flask import render_template
from werkzeug import secure_filename

from labeler import app
from labeler.backend.handle_requests import (getAllImages, getRequiredImages,
                                             isLabelInDb, updateInfo)

STATIC_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/static/'


@app.route("/createLabels", methods=['GET', 'POST'])
def createLabels():
    if flask.request.method == 'POST':
        image = flask.request.files['image']
        label = flask.request.form['label']
        image.save(STATIC_FOLDER + secure_filename(image.filename))
        
        alreadyPresent = isLabelInDb(label, image.filename)   
        
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
            data = [totalImages[0], label]
            return render_template('show_images.html', results=data)


@app.route('/updateLabel', methods=['POST'])
def updateLabel():
    if flask.request.method == 'POST':
        image = flask.request.form['image']
        curr_value = flask.request.form['current_label']
        new_value = flask.request.form['new_label']

        updateInfo(image, curr_value, new_value)
        message = "Label is updated !!"

        return render_template('success.html', message=message)

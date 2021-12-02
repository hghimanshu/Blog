import os
from os.path import dirname, join, realpath

DEBUG = True
WEIGHTS_FOLDER = join(dirname(realpath(__file__)), 'weights/') 
UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'uploaded_images/')
MAX_CONTENT_PATH = 10000000

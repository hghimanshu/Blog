import os
from os.path import join, dirname, realpath

DEBUG = True
UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'uploaded_images/')
MAX_CONTENT_PATH = 10000000
from flask import Flask

from classifier import routes
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

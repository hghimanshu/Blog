from flask import Flask

from flask_bootstrap import Bootstrap
from labeler import routes

app = Flask(__name__)
Bootstrap(app)

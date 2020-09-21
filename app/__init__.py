from flask import Flask
from flask_bootstrap import Bootstrap

# Initializing application
app = Flask(__name__)

from .main import views
from .main import error

from flask import Flask
from flask_bootstrap import Bootstrap

# Initializing application
app = Flask(__name__)

from app import views
from app import error

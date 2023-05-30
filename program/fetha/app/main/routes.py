from flask import render_template
from app.main import bp
from config import Config
import os

#PHOTOS = os.path.join('static', 'photos')

@bp.route('/')
def index():
    return '<h1> AFRICA </h1>'

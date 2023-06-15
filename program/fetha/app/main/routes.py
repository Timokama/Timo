from flask import render_template, url_for
from app.main import bp
import os

#PHOTOS = os.path.join('static', 'photos')

@bp.route('/')
def index():
    return render_template("main.html")
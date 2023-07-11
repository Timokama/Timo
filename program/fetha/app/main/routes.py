from flask import render_template, url_for, Flask
from app.main import bp

@bp.route('/')
def index():
    return render_template("main.html")
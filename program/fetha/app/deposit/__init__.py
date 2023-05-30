from flask import Blueprint

bp = Blueprint('deposit', __name__)


from app.deposit import routes
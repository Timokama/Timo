from flask import Blueprint

bp = Blueprint('family', __name__)


from app.family import routes
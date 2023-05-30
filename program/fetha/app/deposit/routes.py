from flask import render_template, request, redirect
from app.deposit import bp
from app.extensions import db
from app.models.register import Register
from app.models.deposit import Deposit

@bp.route('/')
def index():
    register = Register.query.all()
    deposit = Deposit.query.all()
    return render_template('register/index.html', register=register, deposit = deposit)


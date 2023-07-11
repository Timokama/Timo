from flask import render_template, url_for
from app.reports import bp
from app.extensions import db
from app.models.deposit import Deposit

@bp.route('/')
def index():
    deposit = Deposit.query.all()
    total = 0
    for money in deposit:
        total += money.amount

    count = 0
    for members in deposit:
        member = members.family
        count += 1
    
    return render_template("reports/index.html", total = total, members = count)
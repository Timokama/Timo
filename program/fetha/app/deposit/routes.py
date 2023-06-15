from flask import render_template, request, redirect, url_for
from app.deposit import bp
from app.extensions import db
from app.models.register import Register
from app.models.deposit import Deposit

@bp.route('/')
def index():
    deposit = Deposit.query.all()

    return render_template('register/index.html', deposit = deposit)

@bp.route('/<int:depo_id>/')
def deposit(depo_id):
    register = Register.query.get_or_404(depo_id)
    # depo_id = register.deposit.id
    # depo = Deposit.query.got_or_404(depo_id)

    return render_template('deposit/deposit.html', register=register)

@bp.post('/<int:depo_id>/delete')
def delete(depo_id):
    depo = Deposit.query.get_or_404(depo_id)
    # deposit = Deposit.query.get_or_404(depo_id)
    # deposit_id = depo.family.id
    db.session.delete(depo)
    # db.session.delete(deposit)
    db.session.commit()
    return redirect(url_for('deposit.index'))
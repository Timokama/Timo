from flask import render_template, request, redirect, url_for
from app.deposit import bp
from app.extensions import db
from app.models.register import Register
from app.models.deposit import Deposit
from app.models.wife import Wife
from app.models.child import Child

@bp.route('/')
def index():
    deposit = Deposit.query.all()
    register = Register.query.all()

    return render_template('deposit/index.html', register = register,deposit = deposit)

@bp.route('/<int:depo_id>/')
def deposit(depo_id):
    depo = Deposit.query.get_or_404(depo_id)
    register = Register.query.get_or_404(depo_id)
    # depo_id = register.deposit.id
    
    return render_template('deposit/deposit.html', register = register, deposit = depo)

@bp.route('/<int:depo_id>/edit', methods=('POST', 'GET'))
def edit(depo_id):
    depo = Deposit.query.get_or_404(depo_id)
    if request.method == 'POST':
        amount  = request.form['amount']

        depo.amount  = amount

        db.session.add(depo)
        db.session.commit()
        
        return redirect(url_for('deposit.index'))
    return render_template("deposit/edit.html", deposit = depo)

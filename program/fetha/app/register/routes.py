from flask import render_template, request, redirect, url_for
from app.register import bp
from app.extensions import db
from app.models.register import Register
from app.models.deposit import Deposit
from app.models.wife import Wife
from app.models.child import Child

@bp.route('/')
def index():
    deposit = Deposit.query.all()
    # depo_id = register.deposit.id
    # dopo = Deposit.query.got_or_404(depo_id)

    return render_template('register/index.html', deposit=deposit)

@bp.route('/<int:depo_id>/')
def deposit(depo_id):
    deposit = Deposit.query.get_or_404(depo_id)
    return render_template("register/deposit.html", deposit = deposit)


@bp.route('/create', methods=('POST', 'GET'))
def create():
    if request.method == 'POST':
        deposit = Deposit(amount=request.form['amount'])
        register = Register(firstname=request.form['firstname'], lastname = request.form['lastname'], date_of_birth=request.form['date_of_birth'], deposit=deposit)
        
        db.session.add_all([deposit, register])
        db.session.commit()
        return redirect(url_for('register.create'))
    return render_template('register/create.html')
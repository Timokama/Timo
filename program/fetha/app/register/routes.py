from flask import render_template, request, redirect, url_for
from app.register import bp
from app.extensions import db
from app.models.register import Register
from app.models.deposit import Deposit

@bp.route('/')
def index():
    register = Register.query.all()
    # depo_id = register.deposit.id
    # dopo = Deposit.query.got_or_404(depo_id)

    return render_template('register/index.html', register=register)

@bp.route('/deposit/<int:deposit_id>/')
def deposit(deposit_id):
    register = Register.query.get_or_404(deposit_id)
    depo_id = register.deposit.id
    depo = Deposit.query.got_or_404(depo_id)

    return render_template('deposit/deposit.html', register=register, deposit=depo)


@bp.route('/create', methods=('POST', 'GET'))
def create():
    if request.method == 'POST':
        register = Register(firstname=request.form['firstname'], lastname = request.form['lastname'], email=request.form['email'], age=request.form['age'])
        deposit = Deposit(amount=request.form['amount'], register=register)
        db.session.add_all([register, deposit])
        db.session.commit()
        return redirect(url_for('register.create'))
    return render_template('register/create.html')
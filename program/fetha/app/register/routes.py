from flask import render_template, request, redirect, url_for
from app.register import bp
from app.extensions import db
from app.models.deposit import Deposit
from app.models.register import Register
from app.models.wife import Wife
from app.models.child import Child

@bp.route('/')
def index():
    deposit = Deposit.query.all()
    # register = Register.query.all()

    return render_template('register/index.html', deposit = deposit)

@bp.route('/<int:depo_id>/')
def deposit(depo_id):
    depo = Deposit.query.get_or_404(depo_id)
    register = Register.query.get_or_404(depo_id)
    # depo_id = register.deposit.id
    
    return render_template('deposit/deposit.html', register=register, deposit = depo)

@bp.route('/create', methods=('POST', 'GET'))
def create():
    if request.method == 'POST':
        deposit = Deposit(amount=request.form['amount'])
        register = Register(firstname=request.form['firstname'], lastname = request.form['lastname'], date_of_birth=request.form['date_of_birth'], deposit=deposit)
        
        db.session.add_all([deposit, register])
        db.session.commit()
        return redirect(url_for('register.create'))
    return render_template('register/create.html')

@bp.post('/<int:depo_id>/delete')
def delete(depo_id):
    depo = Deposit.query.get_or_404(depo_id)
    # deposit = Deposit.query.get_or_404(depo_id)
    deposit_id = depo.family.id
    db.session.delete(depo)
    # db.session.delete(deposit)
    db.session.commit()
    return redirect(url_for('deposit.index', depo_id= deposit_id ))

@bp.route('/<int:depo_id>/create_wife/', methods=('POST','GET'))
def create_wife(depo_id):
    depo = Deposit.query.get_or_404(depo_id)
    # register = Register.query.get_or_404(depo_id)
    if request.method == 'POST':
        # register = Register.query.get_or_404(depo_id)
        new_wife = Wife(firstname = request.form['firstname'], lastname = request.form['lastname'], date_of_birth = request.form['date_of_birth'], register = depo.id)
        db.session.add_all([new_wife])
        db.session.commit()
        return redirect(url_for('register.deposit'))
    return render_template('register/create_wife.html', family = depo)
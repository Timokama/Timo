from flask import render_template, request, redirect, url_for
from app.deposit import bp
from app.register import bp
from app.extensions import db
from app.models.deposit import Deposit
from app.models.register import Register
from app.models.wife import Wife
from app.models.child import Child

@bp.route('/')
def index():
    deposit = Deposit.query.all()
    # depo_id = deposit.id
    # register = Register.query.get_or_404(depo_id)

    return render_template('register/index.html', deposit = deposit)

@bp.route('/<int:depo_id>/')
def deposit(depo_id):
    depo = Deposit.query.get_or_404(depo_id)
    register = Register.query.get_or_404(depo_id)
    # depo_id = register.deposit.id
    
    return render_template('register/deposit.html', deposit = depo, register = register)

@bp.route('/<int:depo_id>/edit', methods=('POST', 'GET'))
def edit(depo_id):
    depo = Deposit.query.get_or_404(depo_id)
    if request.method == 'POST':
        amount  = request.form['amount']

        depo.amount  = amount

        db.session.add(depo)
        db.session.commit()
        
        return redirect(url_for('register.index'))
    return render_template("deposit/edit.html", deposit = depo)

@bp.route('/create', methods=('POST', 'GET'))
def create():
    if request.method == 'POST':
        deposit = Deposit(amount=request.form['amount'])
        register = Register(firstname=request.form['firstname'], lastname = request.form['lastname'], date_of_birth=request.form['date_of_birth'], deposit=deposit)
        
        db.session.add_all([deposit, register])
        db.session.commit()
        return redirect(url_for('register.create'))
    return render_template('register/create.html')

@bp.route('/<int:depo_id>/create_wife/', methods=('POST','GET'))
def create_wife(depo_id):
    depo = Deposit.query.get_or_404(depo_id)
    register = Register.query.get_or_404(depo_id)
    if request.method == 'POST':
        # register = Register.query.get_or_404(depo_id)
        # wife = depo.family.id
        new_wife = Wife(firstname = request.form['firstname'], lastname = request.form['lastname'], date_of_birth = request.form['date_of_birth'], register = register)
        db.session.add_all([new_wife])
        db.session.commit()
        return redirect(url_for('register.deposit', depo_id = depo.id))
    return render_template('register/create_wife.html')

@bp.route('/<int:depo_id>/create_child/', methods=('POST','GET'))
def create_child(depo_id):
    depo = Deposit.query.get_or_404(depo_id)
    register = Register.query.get_or_404(depo_id)
    if request.method == 'POST':
        # register = Register.query.get_or_404(depo_id)
        # wife = depo.family.id
        new_child = Child(firstname = request.form['firstname'], lastname = request.form['lastname'], date_of_birth = request.form['date_of_birth'], child = register)
        db.session.add_all([new_child])
        db.session.commit()
        return redirect(url_for('register.deposit', depo_id = depo.id))
    return render_template('register/create_child.html')

@bp.post('/<int:depo_id>/delete/')
def delete(depo_id):
    depo = Deposit.query.get_or_404(depo_id)
    register = Register.query.get_or_404(depo_id)
    for man in depo.family:
        for child in man.child:
            db.session.delete(child)
    for wife in man.wife:
        for child_ in wife.child:
            db.session.delete(child_)
        db.session.delete(wife)
    
    db.session.delete(man)
    db.session.delete(depo)
    db.session.commit()
    return redirect(url_for('register.index'))

from flask import render_template, request, redirect, url_for
# from app.register import bp
from datetime import date
from app.family import bp
from app.extensions import db
from app.models.register import Register
from app.models.deposit import Deposit
from app.models.child import Child
from app.models.wife import Wife


@bp.route('/')
def index():
    family = Deposit.query.all()
    return render_template("family/index.html", family = family)


@bp.route('/<int:depo_id>/')
def family(depo_id):
    family = Deposit.query.get_or_404(depo_id)
    register = Register.query.get_or_404(depo_id)
    # depo_id = register.deposit.id
    # depo = Deposit.query.got_or_404(depo_id)

    return render_template('family/family.html', family = family, register = register)

@bp.route('/<int:depo_id>/edit', methods=('POST', 'GET'))
def edit(depo_id):
    register = Register.query.get_or_404(depo_id)
    if request.method == 'POST':
        firstname=request.form['firstname']
        lastname=request.form['lastname']
        date_of_birth=request.form['date_of_birth']

        register.firstname = firstname
        register.lastname = lastname
        register.date_of_birth = date_of_birth

        db.session.add(register)
        db.session.commit()
        return redirect(url_for('family.family', depo_id=register.id))
    return render_template('family/edit.html', register = register)

@bp.route('/<int:depo_id>/create_wife', methods=('POST', 'GET'))
def create_wife(depo_id):
    register = Register.query.get_or_404(depo_id)
    if request.method == 'POST':
        wife = Wife(
            firstname=request.form['firstname'],
            lastname=request.form['lastname'],
            date_of_birth=request.form['date_of_birth'],
            register = register
        )
        db.session.add(wife)
        db.session.commit()
        return redirect(url_for('family.family', depo_id = register.id))
    return render_template('register/create_wife.html', register=register)

@bp.route('/<int:depo_id>/<int:wife_id>/create_child', methods=('POST', 'GET'))
def create_child(depo_id, wife_id):
    register = Register.query.get_or_404(depo_id)
    wife = Wife.query.get_or_404(wife_id)
    if request.method == 'POST':
        child = Child(
            firstname=request.form['firstname'],
            lastname=request.form['lastname'],
            date_of_birth=request.form['date_of_birth'],
            wife = wife
        )
        db.session.add(child)
        db.session.commit()
        return redirect(url_for('family.family', depo_id = register.id))
    return render_template('family/create_child.html', register=register, wife = wife)

@bp.post('/<int:depo_id>/<int:del_id>/delete')
def delete(depo_id, del_id):
    register = Register.query.get_or_404(depo_id)
    wife = Wife.query.get_or_404(del_id)
    for child in wife.child:
        db.session.delete(child)
    db.session.delete(wife)
    db.session.commit()
    return redirect(url_for('family.family', depo_id = register.id))

@bp.route('/<int:depo_id>/<int:edit_id>/edit_wife', methods=('POST','GET'))
def edit_wife(depo_id, edit_id):
    # depo = Deposit.query.get_or_404(depo_id)
    register = Register.query.get_or_404(depo_id)
    wife = Wife.query.get_or_404(edit_id)
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        date_of_birth = request.form['date_of_birth']
        
        wife.firstname = firstname
        wife.lastname = lastname
        wife.date_of_birth = date_of_birth

        db.session.add(wife)
        db.session.commit()

        return redirect(url_for('family.family', depo_id = register.id))
    return render_template('family/edit_wife.html', wife = wife, register = register)

@bp.route('/<int:depo_id>/<int:edit_id>/<int:child_id>/edit_child', methods=('POST','GET'))
def edit_child(depo_id, edit_id, child_id):
    # depo = Deposit.query.get_or_404(depo_id)
    register = Register.query.get_or_404(depo_id)
    wife = Wife.query.get_or_404(edit_id)
    child = Child.query.get_or_404(child_id)
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        date_of_birth = request.form['date_of_birth']
        
        child.firstname = firstname
        child.lastname = lastname
        child.date_of_birth = date_of_birth

        db.session.add(child)
        db.session.commit()

        return redirect(url_for('family.family', depo_id = register.id))
    return render_template('family/edit_child.html', wife = wife, register = register, child = child)

@bp.route('/<int:depo_id>/<int:child_id>/edit_child', methods=('POST','GET'))
def editchild(depo_id, child_id):
    # depo = Deposit.query.get_or_404(depo_id)
    register = Register.query.get_or_404(depo_id)
    child = Child.query.get_or_404(child_id)
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        date_of_birth = request.form['date_of_birth']

        child.firstname = firstname
        child.lastname = lastname
        child.date_of_birth = date_of_birth
        child.child = register

        db.session.add(child)
        db.session.commit()

        return redirect(url_for('family.family', depo_id = register.id))
    return render_template('family/edit_child.html', register = register, child = child)

@bp.post('/<int:depo_id>/delete/')
def delete_family(depo_id):
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
    return redirect(url_for('family.index'))

@bp.route('/<int:depo_id>/age')
def date_of_b(depo_id):
        deposit = Deposit.query.get_or_404(depo_id)
        register = Register.query.get_or_404(depo_id)
        today = date.today()
        d3 = today.strftime("%m-%d-%y")
        d4 = register.date_of_birth
        # d4 = d_4.strftime(d_4"%m-%d-%Y")
        # print("d3 =", d3)
        age = d3.year - d4.year - ((today.month, today.day) < (d4.month, d4.day))

        return render_template("family/birthday.html", deposit = deposit, register = register, age=age)
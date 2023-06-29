from flask import render_template, request, redirect, url_for
from app.register import bp
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
    # depo_id = register.deposit.id
    # depo = Deposit.query.got_or_404(depo_id)

    return render_template('family/family.html', family = family)

@bp.route('/<int:depo_id>/', methods=('GET', 'POST'))
def wife(depo_id):
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
        return redirect(url_for('family.family', depo_id=register.id))
    return render_template('family/create_wife.html', register=register)

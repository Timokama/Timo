from app.extensions import db
#from app.models.register import Register

class Deposit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer)

    pin_id = db.Column(db.Integer, db.ForeignKey('register.id'))

    def __repr__(self):
        return f'<Amount {self.amount} >'
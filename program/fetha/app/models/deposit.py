from app.extensions import db

class Deposit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer)

    family = db.relationship('Register', backref='deposit')
    
    def __repr__(self):
        return f'<Amount {self.amount} >'
from app.extensions import db
from sqlalchemy.sql import func
# from app.models.deposit import Deposit

class Register(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    age = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    deposit = db.relationship('Deposit', backref='register')
    
    def __repr__(self):
        return f'<Member {self.firstname}>'
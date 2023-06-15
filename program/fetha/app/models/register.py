from app.extensions import db
# from datetime import date
from sqlalchemy.sql import func


class Register(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.String(10))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    wife = db.relationship('Wife', backref='register')
    depo_id = db.Column(db.Integer, db.ForeignKey('deposit.id'))
    
    
    # child = db.relationship('Child', backref='child')
    
    # def __init__(self, firstname, lastname, age):
    #     self.firstname = firstname
    #     self.lastname = lastname
    #     self.age = age

    def __repr__(self):
        return f'<Member {self.firstname}>'

    # def age(date_birth):
    #     today = date.today()
    #     date = today.year - date_birth.year - ((today.month, today.day)<(date_birth.month,date_birth.day))
    #     return (date)
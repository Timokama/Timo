from app.extensions import db
from datetime import datetime
from sqlalchemy.sql import func


class Register(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.String(10))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    wife = db.relationship('Wife', backref='register')
    child = db.relationship('Child', backref='child')
    depo_id = db.Column(db.Integer, db.ForeignKey('deposit.id'))
    
    def __repr__(self):
        return f'<Member {self.firstname}>'
    
    # def __init__(self, firstname, lastname, date_of_birth: datetime, deposit):
    #     self.firstname = firstname
    #     self.lastname = lastname
    #     self.date_of_birth= date_of_birth
    #     self.deposit = deposit

    

    # def age(date_birth):
    #     today = date.today()
    #     date = today.year - date_birth.year - ((today.month, today.day)<(date_birth.month,date_birth.day))
    #     return (date)
from app.extensions import db
from datetime import date
from sqlalchemy.sql import func

# from app.models.deposit import Deposit

class Wife(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.String(10))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    child = db.relationship('Child', backref='wife')
    register_id = db.Column(db.Integer, db.ForeignKey('register.id'))
    
    
    
    def __repr__(self):
        return f'<Member {self.firstname}>'

    # def age(date_birth):
    #     today = date.today()
    #     age = today.year - date_birth.year - ((today.month, today.day)<(date_birth.day))
    #     return (age)
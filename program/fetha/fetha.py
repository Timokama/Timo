from app.extensions import db
from app.models.deposit import Deposit
from app.models.register import Register
from app.models.wife import Wife
from app.models.child import Child

db.drop_all()
db.create_all()

depo1 = Deposit(amount=1000)
reg1 = Register(firstname="Timothy", lastname="Kamau", date_of_birth="2001-19-05", deposit=depo1)
wife1 = Wife(firstname="Null", lastname="Null", date_of_birth="2001-19-05",register=reg1)
child1 = Child(firstname="Null", lastname="Null",date_of_birth="2001-19-05", wife=wife1)

depo2 = Deposit(amount=1000)
reg2 = Register(firstname="Mark", lastname="Waweru", date_of_birth="2001-19-05", deposit=depo2)
wife2 = Wife(firstname="Null", lastname="Null", date_of_birth="2001-19-05",register=reg2)
child2 = Child(firstname="Null", lastname="Null", date_of_birth="2001-19-05",wife=wife2)

db.session.add_all([reg1, depo1,wife1, child1])
db.session.add_all([reg2, depo2,wife2, child2])
db.session.commit()
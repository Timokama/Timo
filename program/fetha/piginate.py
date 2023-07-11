from app.extensions import db
from app.models.deposit import Deposit
from app.models.register import Register
from app.models.wife import Wife
from app.models.child import Child
from datetime import date

depo = Deposit.query.all()
for money in depo:
    print(f'{money.amount}')
    for man in money.family:
        print(f'{man.firstname}, {man.lastname}, Date: {man.date_of_birth}')
        for wife in man.wife:
            print(f'{wife.firstname}, {wife.lastname} Date: {wife.date_of_birth}')
            for child in wife.child:
                print(f'{child.firstname}, {child.lastname}, Date: {child.date_of_birth}')
    print('----------')

for man in depo:
    for d in man.family:
        dates = d.date_of_birth

def age(dates):
    today = date.today()
    age = today.year - dates.date_of_birth.year - ((today.month, today.day)<(dates.date_of_birth.month, dates.date_of_birth.day))
    return(age)

print(age())
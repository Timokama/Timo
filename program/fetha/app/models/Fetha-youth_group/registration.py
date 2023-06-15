import csv
from datetime import date

class Registration:
    all = []
    def __init__(self, name: str, reg_fee: float, deposit: float, age: date):
        #Runs validation to the resived arguments
        # assert age >= 18,f"{age} is too young 18+ years"
        # assert age <= 35, f"Age {age} is old to have an account"
        
        #Assign to self object
        self.name = name
        self.reg_fee = reg_fee
        self.deposit = deposit
        self.age = age

        #Action Execute
        Registration.all.append(self)
    def age(d_of_birth):
        today = date.today()
        d3 = today.strftime("%m/%d/%y")
        # print("d3 =", d3)
        age1 = d3.year - d_of_birth.year - ((today.month, today.day) < (d_of_birth.month, d_of_birth.day))
        #assert age <= 18 or age >=35, f"Fetha youth group recognises members age between 18 and 35"
        try:
            if age1 <= 18 or age1 >= 35:
               print("age <= 18 or age >=35, Fetha youth group recognises members age between 18 and 35")
        finally:
            return age1
        
        
    def total_share(self):
        return self.reg_fee + self.deposit

    # @classmethod
    # def file_csv(self):
    #     with open('reg.csv') as file:
    #         reader = csv.DictReader(file, delimiter=':')
    #         for row in reader:
    #             print(row)
    #         Registrations = list(reader)
        
    #     for name, reg_fee, deposit, age in reader:
    #         all.append({"name":name, "reg_fee":reg_fee, "deposit":deposit, "age": age})

    #         for reg in Registrations :
    #             reg(
    #                 name=reg.get('name'),
    #                 reg_fee=float(reg.get('reg_fee')),
    #                 deposit=float(reg.get('deposit')),
    #                 agge=float(reg.get('age'))
    #             )
    #             print(f"Name: {'name'}, reg_fee: {'reg_fee'}, deposit: {'deposit'}")

    def __repr__(self):
        return f"Registred '{self.name}', {self.reg_fee}, {self.deposit}, {self.age}"
#Registration.file_csv()
reg1=Registration('Timothy',100,500, 2001/19/5)
reg2=Registration('John',100,500, 2001/20/5)
print(reg1.age)
print(reg2.age)
#Registration.file_csv()
#print(Registration.all)
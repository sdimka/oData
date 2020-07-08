from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import create_engine, ForeignKey

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

from datetime import datetime, date, time

engine = create_engine('mysql+mysqlconnector://root:mypassword@192.168.1.180')
engine.execute("CREATE DATABASE IF NOT EXISTS alchem")  # create db
engine.execute("USE alchem")
Base = declarative_base()


class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    name = Column(String(25))
    address = Column(String(25))
    email = Column(String(25))


class Invoice(Base):
    __tablename__ = 'invoices'

    id = Column(Integer, primary_key=True)
    custid = Column(Integer, ForeignKey('customers.id'))
    invno = Column(Integer)
    amount = Column(Integer)
    customer = relationship("Customer", back_populates="invoices")


Customer.invoices = relationship("Invoice", order_by=Invoice.id, back_populates="customer")
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# c1 = Customers(date=datetime.now(), name='Ravi Kumar', address='Station Road Nanded', email='ravi@gmail.com')
#
# session.add(c1)
# session.commit()
#
# session.add_all([
#     Customers(date=datetime.now(), name='Komal Pande', address='Koti, Hyderabad', email='komal@gmail.com'),
#     Customers(date=datetime.now(), name='Rajender Nath', address='Sector 40, Gurgaon', email='nath@gmail.com'),
#     Customers(date=datetime.now(), name='S.M.Krishna', address='Budhwar Peth, Pune', email='smk@gmail.com')]
# )
# session.commit()

result = session.query(Customer).filter(Customer.name == 'Komal Pande').\
    filter(Customer.date == '2020-07-08 01:08:52')

for row in result:
    print("Date:", row.date, "Name: ", row.name, "Address:", row.address, "Email:", row.email)

result = session.query(Customer).filter(Customer.id.in_([1, 3]))
for row in result:
    print("ID:", row.id, "Name: ", row.name, "Address:", row.address, "Email:", row.email)


result = session.query(Customer).filter(Customer.id > 2, Customer.name.like('Ra%'))
for row in result:
   print ("ID:", row.id, "Name: ",row.name, "Address:",row.address, "Email:",row.email)

c1 = session.query(Customer).get(1)
print("ID:", c1.id, "Name: ", c1.name, "Address:", c1.address, "Email:", c1.email, c1.invoices)
# c1.invoices = [Invoice(invno = 10, amount = 15000), Invoice(invno = 14, amount = 3850)]
# session.commit()

for c, i in session.query(Customer, Invoice).filter(Customer.id == Invoice.custid).all():
   print ("ID: {} Name: {} Invoice No: {} Amount: {}".format(c.id,c.name, i.invno, i.amount))

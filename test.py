import bd_engine as bd
from datetime import datetime, date, timedelta

bd.fake_bd_gen()
# dt = date.today() - timedelta(5)
# print(dt)




#from order_repo import Order, Product, Customer, session
# from datetime import datetime, date, time
#
#
# o1 = Order(date=datetime.now(), number=154)
# o1.customer = Customer(name='Ivanov Ivan', e_mail='sss@mmm.com')
# o1.products = [Product(name='Супер крем', quantity=2, price=25), Product(name='Супер ifvgeym', quantity=3, price=15)]
#
# session.add(o1)
# session.commit()



"""
from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, Boolean
from sqlalchemy import create_engine, ForeignKey

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

from datetime import datetime, date, time

engine = create_engine('mysql+mysqlconnector://root:mypassword@192.168.1.180')
engine.execute("CREATE DATABASE IF NOT EXISTS alchem")  # create db
engine.execute("USE alchem")
Base = declarative_base()


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    number = Column(Integer)
    # client -
    customer_id = Column(Integer, ForeignKey('customers.id'))
    customer = relationship("Customer", back_populates="orders")

    # products -
    products = relationship("Product", back_populates="order")

    total_sum = Column(DECIMAL(18, 4))
    total_quantity = Column(DECIMAL(18, 4))
    isPayed = Column(Boolean)
    payType = Column(Integer)


class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    last_name = Column(String(50))
    e_mail = Column(String(50))
    phone = Column(String(25))
    orders = relationship("Order", back_populates="customer")


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    quantity = Column(DECIMAL(18, 4))
    price = Column(DECIMAL(18, 4))
    cost_price = Column(DECIMAL(18, 4))

    order_id = Column(Integer, ForeignKey('orders.id'))
    order = relationship("Order", back_populates="products")


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

o1 = Order(date=datetime.now(), number=154)
o1.customer = Customer(name='Ivanov Ivan', e_mail='sss@mmm.com')
o1.products = [Product(name='Супер крем', quantity=2, price=25), Product(name='Супер ifvgeym', quantity=3, price=15)]

session.add(o1)
session.commit()
"""

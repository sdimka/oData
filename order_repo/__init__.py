__all__ = ['Order', 'Customer', 'Product']

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


engine = create_engine('mysql+mysqlconnector://root:mypassword@192.168.1.180')
engine.execute("CREATE DATABASE IF NOT EXISTS alchem")  # create db
engine.execute("USE alchem")
Base = declarative_base()

from .order import Order
from .product import Product
from .customer import Customer

Order.products = relationship("Product", order_by=Product.id, back_populates="orders")

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()





__all__ = ['Order', 'Customer', 'Product', 'Customer1c', 'session']

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


engine = create_engine('mysql+mysqlconnector://root:mypassword@192.168.1.180', pool_recycle=3600)
engine.execute("CREATE DATABASE IF NOT EXISTS testDB")  # create db alchem
engine.execute("USE testDB")  # alchem
Base = declarative_base()

from .order import Order
from .product import Product
from .customer import Customer
from .customer_1c import Customer1c

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()





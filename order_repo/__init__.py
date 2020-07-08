__all__ = ["bd_engine", "client"]

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql+mysqlconnector://root:mypassword@192.168.1.180')
engine.execute("CREATE DATABASE IF NOT EXISTS alchem")  # create db
engine.execute("USE alchem")
Base = declarative_base()
Base.metadata.create_all(engine)

from .order import Order
from .product import Product
from .customer import Customer

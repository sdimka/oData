from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, Boolean

from order_repo import Base


class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    last_name = Column(String(50))
    e_mail = Column(String(50))
    phone = Column(String(25))

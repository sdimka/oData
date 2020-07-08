from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, Boolean
from sqlalchemy.orm import relationship

from order_repo import Base


class Order(Base):
    __tablename__ = 'orders'

    # date = Column(DateTime)
    # name = Column(String(25))
    # address = Column(String(25))
    # email = Column(String(25))

    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    number = Column(Integer)
    # client -
    customer_id = Column(Integer, ForeignKey('customer.id'))
    # customer = relationship("Customer", back_populates="orders")
    customer = relationship("Customer", backref=backref("orders", uselist=False))
    # products -
    products = relationship("Product", order_by=Product.id, back_populates="orders")
    total_sum = Column(DECIMAL(18, 4))
    total_quantity = Column(DECIMAL(18, 4))
    isPayed = Column(Boolean)
    payType = Column(Integer)

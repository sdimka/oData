from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref

from order_repo import Base


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

    def serialize(self):
        return {'id': self.id,
                'date': self.date,
                'number': self.number,
                'client': str(self.customer.name + ' ' + self.customer.last_name),
                'sum': float(self.total_sum),
                'isPayed': self.isPayed,
                'payType': self.payType}

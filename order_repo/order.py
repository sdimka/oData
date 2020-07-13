from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref

from order_repo import Base


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    b_fuser_id = Column(Integer)  # for bitrix synchronization
    number = Column(Integer)  # bitrix order_id

    delivery_price = Column(Integer)
    order_status = Column(Integer)  # 1 - normal, 2 - canceled, 3 - abandoned
    b_status_id = Column(String(2))  # from bitrix
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
                'client': (str(self.customer.name) if self.customer.name is not None else '') + ' ' + str(self.customer.last_name),
                'sum': float(self.total_sum),
                'totalQuantity': float(self.total_quantity),
                'isPayed': self.isPayed,
                'payType': self.payType,
                'status': self.order_status,
                'isResident': self.customer.is_1C_resident}


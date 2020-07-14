from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship

from order_repo import Base


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    quantity = Column(DECIMAL(18, 4))
    price = Column(DECIMAL(18, 4))
    cost_price = Column(DECIMAL(18, 4))

    order_id = Column(Integer, ForeignKey('orders.id'), index=True)
    order = relationship("Order", back_populates="products")

    tempColumn = Column(Integer)

    def serialize(self):
        return {'id': self.id,
                'name': self.name,
                'quantity': float(self.quantity),
                'price': float(self.price),
                'cost_price': self.cost_price if self.cost_price is not None else ''
                }

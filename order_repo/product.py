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

    # order_id = Column(Integer, ForeignKey('product.id'))
    order = relationship("Order", back_populates="products")

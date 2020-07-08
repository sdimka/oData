from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, Boolean
from sqlalchemy.orm import relationship

from order_repo import Base


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    quantity = Column(DECIMAL(18, 4))
    price = Column(DECIMAL(18, 4))
    cost_price = Column(DECIMAL(18, 4))
    order = relationship("Order", back_populates="products")

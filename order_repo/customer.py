from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, Boolean
from sqlalchemy.orm import relationship

from order_repo import Base


class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    bit_id = Column(Integer)
    name = Column(String(50))
    last_name = Column(String(50))
    e_mail = Column(String(50))
    phone = Column(String(25))
    orders = relationship("Order", back_populates="customer")
    is_1C_resident = Column(Boolean)

    def serialize(self):
        return {'id': self.id,
                'name': self.name + self.last_name,
                'e_mail': self.e_mail,
                'phone': self.phone}

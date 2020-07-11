from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, Boolean
from sqlalchemy.orm import relationship

from order_repo import Base


class Customer1c(Base):
    __tablename__ = 'customers1c'
    id = Column(Integer, primary_key=True)
    code_1c = Column(String(9), index=True)  # АА0217499
    id_1c = Column(String(36))  # abc543af-eddf-11e2-809a-005056950007
    name = Column(String(255))
    dateCreate = Column(DateTime)

    customer = relationship("Customer", back_populates="customer1c")



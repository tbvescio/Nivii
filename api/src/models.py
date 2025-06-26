from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Numeric, Date


Base = declarative_base()

class SalesData(Base):
    __tablename__ = 'sales_data'
    date = Column(Date, primary_key=True)
    week_day = Column(String(20))
    hour = Column(Integer)
    ticket_number = Column(String(100))
    waiter = Column(String(100))
    product_name = Column(String(100))
    quantity = Column(Integer)
    unitary_price = Column(Numeric)
    total = Column(Numeric)


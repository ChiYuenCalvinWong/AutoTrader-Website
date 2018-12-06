from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime

class Auto(Base):
    __tablename__ = 'autos'

    id = Column(Integer, primary_key=True)
    status = Column(String(50))
    year = Column(String(120))
    model = Column(String)
    vin = Column(String)
    price = Column(Integer)

    def __init__(self, status=None, year=None, model=None, vin=None, price=None):
        self.status = status
        self.year = year
        self.model = model
        self.vin = vin
        self.price = price

    def __repr__(self):
        return '<Auto %r>' % (self.auto)

class Bought(Base):
    __tablename__ = 'boughts'
    id = Column(Integer, primary_key=True)
    status = Column(String)
    year = Column(String)
    model = Column(String)
    vin = Column(String)
    price = Column(Integer)

    def __init__(self, status=None, year=None, model=None, vin=None, price=None):
        self.status = status
        self.year = year
        self.model = model
        self.vin = vin
        self.price = price

    def __repr__(self):
        return '<Bought %r>' % (self.bought)


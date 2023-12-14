from sqlalchemy import Column, Integer, String, Float

from src.utils import Base


class Locations(Base):
    __tablename__ = 'locations'

    atm_id = Column(Integer, primary_key=True)
    latitude = Column(Float)
    longitude = Column(Float)
    address = Column(String(128))


class Statistics(Base):
    __tablename__ = 'statistics'

    atm_id = Column(Integer, primary_key=True)
    services_per_day = Column(Integer)
    amount_per_day = Column(Float)

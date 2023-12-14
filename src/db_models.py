from sqlalchemy import Column, Integer, String, Float, Boolean, Date, ForeignKey

from src.wmts.database import Base


class ATM(Base):
    __tablename__ = 'atm'

    atm_id = Column(Integer, primary_key=True)
    location_name = Column(String(100))
    latitude = Column(Float)
    longitude = Column(Float)
    address = Column(String(255))
    city = Column(String(100))
    state = Column(String(50))
    country = Column(String(50))
    is_operational = Column(Boolean)
    last_service_date = Column(Date)


class ATMStatistics(Base):
    __tablename__ = 'atm_statistics'

    stats_id = Column(Integer, primary_key=True)
    atm_id = Column(Integer, ForeignKey('atm.atm_id'))
    transaction_date = Column(Date)
    total_transactions = Column(Integer)
    successful_transactions = Column(Integer)
    failed_transactions = Column(Integer)

    # Establish a relationship with the ATM table
    # atm = relationship("ATM", back_populates="atm_statistics")


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

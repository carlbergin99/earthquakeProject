# Script to initialize schemas for SQL database
from sqlalchemy import create_engine, Column, Integer, Float, String, ForeignKey, DECIMAL, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os

Base = declarative_base()


class EarthquakeEvent(Base):
    __tablename__ = 'earthquake_events'
    event_id = Column(Integer, primary_key=True, autoincrement=True)
    observation_time = Column(TIMESTAMP, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    magnitude = Column(DECIMAL(4, 2), nullable=False)
    depth = Column(DECIMAL(6, 2), nullable=False)
    place_name = Column(String(255), nullable=False)


class EventMunicipality(Base):
    __tablename__ = 'event_municipalities'
    id = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(Integer, ForeignKey('earthquake_events.event_id'), nullable=False)
    prefecture = Column(String(255), nullable=False)
    seismic_intensity = Column(DECIMAL(2, 1))
    municipality = Column(String(255), nullable=False)
    earthquake_event = relationship("EarthquakeEvent", back_populates="municipalities")


EarthquakeEvent.municipalities = relationship("EventMunicipality", order_by=EventMunicipality.id, back_populates="earthquake_event")


def main():
    # Configure your database URI here
    DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///earthquake_data.db')

    engine = create_engine(DATABASE_URI, echo=True)
    Base.metadata.create_all(engine)

#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.city import City
from os import getenv


class State(BaseModel, Base):
    """State class"""

    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship("City", cascade="all", backref="state")
    if getenv("HBNB_TYPE_STORAGE") != "db":

        @property
        def cities(self):
            from models import storage

            all_cities = storage.all(City)
            state_cities = []
            for city in all_cities.values():
                if self.id == city.state_id:
                    state_cities.append(city)
            return state_cities

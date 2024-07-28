#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from models.review import Review
from models.amenity import Amenity
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from os import getenv

place_amenity = Table(
    "place_amenity",
    Base.metadata,
    Column(
        "place_id",
        String(60),
        ForeignKey("places.id"),
        nullable=False,
        primary_key=True,
    ),
    Column(
        "amenity_id",
        String(60),
        ForeignKey("amenities.id"),
        nullable=False,
        primary_key=True,
    ),
)


class Place(BaseModel, Base):
    """A place to stay"""

    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, nullable=False)
    number_bathrooms = Column(Integer, nullable=False)
    max_guest = Column(Integer, nullable=False)
    price_by_night = Column(Integer, nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)
    amenity_ids = []
    city = relationship("City", back_populates="places")
    reviews = relationship("Review", cascade="all", backref="place")
    amenities = relationship(
        "Amenity", secondary=place_amenity, backref="place_amenity", viewonly=False
    )
    if getenv("HBNB_TYPE_STORAGE") != "db":

        @property
        def reviews(self):
            from models import storage

            all_reviews = storage.all(Review)
            place_reviews = []
            for review in all_reviews.values():
                if self.id == review.place_id:
                    place_reviews.append(review)
            return place_reviews

        @property
        def amenities(self):
            from models import storage

            amenities_list = []
            all_amenities = storage.all()
            for key, amenity in all_amenities.items():
                if key in self.amenity_ids:
                    amenities_list.append(amenity)
            return amenities_list

        @amenities.setter
        def amenities(self, obj=None):
            if type(obj).__name__ == "Amenity":
                key = "Amenity" + "." + obj.id
                self.amenity_ids.append(key)

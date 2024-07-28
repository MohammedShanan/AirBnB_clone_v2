#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid

from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime, VARCHAR


Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""

    id = Column(String(60), primary_key=True, unique=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        from models import storage

        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            self.save()
        else:
            self.__set_attr(kwargs)
            self.save()

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split(".")[-1]).split("'")[0]
        return "[{}] ({}) {}".format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage

        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({"__class__": (str(type(self)).split(".")[-1]).split("'")[0]})
        dictionary["created_at"] = self.created_at.isoformat()
        dictionary["updated_at"] = self.updated_at.isoformat()
        if "_sa_instance_state" in dictionary.keys():
            del dictionary["_sa_instance_state"]
        return dictionary

    def __set_attr(self, attr_dict):
        """
        private: converts attr_dict values to python class attributes
        """
        if "id" not in attr_dict:
            attr_dict["id"] = str(uuid.uuid4())
        if "created_at" not in attr_dict:
            attr_dict["created_at"] = datetime.utcnow()
        elif not isinstance(attr_dict["created_at"], datetime):
            attr_dict["created_at"] = datetime.fromisoformat(attr_dict["created_at"])
        if "updated_at" not in attr_dict:
            attr_dict["updated_at"] = datetime.utcnow()
        elif not isinstance(attr_dict["updated_at"], datetime):
            attr_dict["updated_at"] = datetime.fromisoformat(attr_dict["updated_at"])
        if "__class__" in attr_dict.keys():
            attr_dict.pop("__class__")
        for attr, value in attr_dict.items():
            setattr(self, attr, value)

    def delete(self):
        """delete obj from __objects if it’s inside"""
        from models import storage

        storage.delete(self)

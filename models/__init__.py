#!/usr/bin/python3
"""This module instantiates an object of class FileStorage"""
from os import environ
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage


if environ["HBNB_TYPE_STORAGE"] == "db":
    from models.engine.db_storage import DBStorage

    storage = DBStorage()
    storage.reload()

else:  # file storage selected
    from models.engine.file_storage import FileStorage

    storage = FileStorage()
    storage.reload()

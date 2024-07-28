#!/usr/bin/python3
"""This module defines a New engine DBStorage"""

from models.base_model import Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from os import getenv


class DBStorage:
    """database storage engine"""

    __engine = None
    __session = None

    def __init__(self):
        """create the  engine"""
        user = getenv("HBNB_MYSQL_USER")
        password = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        db = getenv("HBNB_MYSQL_DB")
        self.__engine = create_engine(
            "mysql+mysqldb://{}:{}@{}/{}".format(user, password, host, db),
            pool_pre_ping=True,
        )
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query the database and return a dictionary"""
        objs = []
        classes = [State, City, User, Place, Review, Amenity]
        if cls:
            if isinstance(cls, str):
                cls = eval(cls)
            objs = self.__session.query(cls).all()
        else:
            for cls in classes:
                objs.extend(self.__session.query(cls).all())
        return {type(obj).__name__ + "." + obj.id: obj for obj in objs}

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj:
            cls_name = type(obj).__name__
            cls_name = eval(cls_name)
            obj = self.__session.query(cls_name).filter(cls_name.id == obj.id)
            self.__session.delete(obj.first())

    def reload(self):
        """create all tables in the database and create
        the current database session"""
        Base.metadata.create_all(self.__engine)
        session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session)
        self.__session = Session()

    def close(self):
        """Close current session"""
        self.__session.close()

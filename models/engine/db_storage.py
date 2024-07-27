#!/usr/bin/python3
"""Defines the DBStorage engine"""
from os import getenv
from models.base_model import Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker


class DBStorage:
    """database storage engine"""

    __engine = None
    __session = None

    def __init__(self):
        """Initialize a new DBStorage instance"""
        self.__engine = create_engine(
            "mysql+mysqldb://{}:{}@{}/{}".format(
                getenv("HBNB_MYSQL_USER"),
                getenv("HBNB_MYSQL_PWD"),
                getenv("HBNB_MYSQL_HOST"),
                getenv("HBNB_MYSQL_DB"),
            ),
            pool_pre_ping=True,
        )
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query all objects by class name"""
        classes = [State, City, User, Place, Review, Amenity]
        objs = []
        if cls is None:
            for cls in classes:
                objs.extend(self.__session.query(cls).all())
        else:
            objs = self.__session.query(cls).all()
        return {type(obj).__name__ + "." + obj.id: obj for obj in objs}

    def new(self, obj):
        """Add obj to current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes to the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete obj from current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database and initialize new session"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Close current session"""
        self.__session.close()

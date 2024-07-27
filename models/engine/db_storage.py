#!/usr/bin/python3
"""This module defines a New engine DBStorage"""


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base_model import Base
from os import getenv


class DBStorage:
    """database storage engine"""

    __engine = None
    __session = None

    def __init__(self):
        user = getenv("HBNB_MYSQL_USER")
        password = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        db = getenv("HBNB_MYSQL_DB")
        self.__engine = create_engine(
            "mysql+mysqldb:{}:{}@{}/{}".format(user, password, host, db),
            pool_pre_ping=True,
        )
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

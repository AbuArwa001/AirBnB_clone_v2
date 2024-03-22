#!/usr/bin/python3
"""This module defines a class to manage database storage for hbnb clone"""
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models.base_model import Base
from models.place import Place
from models.city import City
from models.user import User
from models.state import State
from models.amenity import Amenity
from models.review import Review
from os import getenv


class DBStorage:
    """This class manages storage of hbnb models in mysql database"""

    __engine = None
    __session = None

    def __init__(self):
        """Creates the engine"""
        dialect = 'mysql'
        driver = 'mysqldb'
        env = getenv('HBNB_ENV')
        user = getenv('HBNB_MYSQL_USER')
        password = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        db_name = getenv('HBNB_MYSQL_DB')
        self.__engine = create_engine("{}+{}://{}:{}@{}/{}".format(
            dialect, driver, user, password, host, db_name
        ), pool_pre_ping=True)

        if env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query all objects depending of the class name"""
        classes = {
            'State': State,
            'City': City,
            'User': User,
            'Amenity': Amenity,
            'Place': Place,
            # 'Review': Review
        }

        objects = {}
        if cls and cls in classes:
            result = self.__session.query(classes[cls]).all()
            for obj in result:
                key = "{}.{}".format(cls, obj.id)
                objects[key] = obj
        else:
            for class_name, class_obj in classes.items():
                result = self.__session.query(class_obj).all()
                for obj in result:
                    key = "{}.{}".format(class_name, obj.id)
                    objects[key] = obj
        return objects

    def new(self, obj):
        """Adds an object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commits all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes from the current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """
        Creates all tables in the database and also creates the current
        database session
        """
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(
            sessionmaker(
                bind=self.__engine,
                expire_on_commit=False
            )
        )

    def close(self):
        """Closes the current SQLAlchemy session"""
        self.__session.close()

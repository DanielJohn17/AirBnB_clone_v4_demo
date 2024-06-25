#!/usr/bin/python3
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.base_model import BaseModel, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv
from dotenv import load_dotenv

classes_dict = {"User": User,
                "State": State,
                "City": City,
                "Amenity": Amenity,
                "Place": Place,
                "Review": Review
                }


class DBStorage:
    __engine = None
    __session = None
    
    def __init__(self):

        load_dotenv() # load the .env file
        
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".
                                      format(HBNB_MYSQL_USER, 
                                             HBNB_MYSQL_PWD,
                                             HBNB_MYSQL_HOST,
                                             HBNB_MYSQL_DB), pool_pre_ping=True)
        
        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):

        new_dict = {}
        for clss in classes_dict.keys():
            if cls is None or cls == classes_dict[clss] or cls is clss:
                objs = self.__session.query(classes_dict[clss]).all()
                for obj in objs:
                    key = "{}.{}".format(obj.__class__.__name__, obj.id)
                    new_dict[key] = obj

        return new_dict

    def new(self, obj):
        self.__session.add(obj)

    def save(self):
        self.__session.commit()

    def reload(self):
        Base.metadata.create_all(self.__engine)
        Sess = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(Sess)
        
        self.__session = Session

    def delete(self, obj=None):
        if obj is not None:
            self.__session.delete(obj)

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()

    def get(self, cls, id):
        if type(cls) is str and type(id) is str and cls in classes_dict:
            cls_object = self.__session.query(classes_dict[cls]).filter_by(id=id).first()
            return cls_object

        return None
    
    def count(self, cls=None):
        if cls:
            total_objects = self.__session.query(classes_dict[cls]).count()
        else:
            for clss in classes_dict.values():
                total_objects = self.__session.query(clss).count()

        return total_objects

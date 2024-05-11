#!/usr/bin/python3
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, String
import models

t_format = "%Y-%m-%dT%H:%M:%S.%f"

if models.storage_t == "db":
    Base = declarative_base()
else:
    Base = object


class BaseModel:
    if models.storage_t == "db":
        id = Column(String(60), primary_key=True)
        created_at = Column(DateTime, default=datetime.utcnow)
        updated_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = self.created_at
        else:
            if "id" not in kwargs:
                self.id = str(uuid.uuid4())
            if "created_at" not in kwargs:
                self.created_at = datetime.utcnow()
            if "updated_at" not in kwargs:
                self.updated_at = datetime.utcnow()

            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    value = datetime.strptime(kwargs[key], t_format)
                if key != "__class__":
                    setattr(self, key, value)

    def save(self):
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()


    def to_dict(self):
        dic = {}
 
        for key, value in self.__dict__.items():
            if key == 'created_at' or key == 'updated_at':
                dic[key] = value.strftime(t_format)
            else:
                if not value:
                    pass
                else:
                    dic[key] = value
        dic["__class__"] = self.__class__.__name__
        if "_sa_instance_state" in dic.keys():
            del dic["_sa_instance_state"]

        return dic

    def __str__(self):
        c_name = self.__class__.__name__
        return "[{:s}] ({:s}) {}".format(c_name, self.id, self.__dict__)

    def delete(self):
        models.storage.delete(self)


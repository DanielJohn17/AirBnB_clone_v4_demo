#!/usr/bin/python3
from models.base_model import BaseModel, Base
import models
from models.city import City
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

class State(BaseModel, Base):
    if models.storage_t == "db":
        __tablename__ = "states"
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state", cascade="all, delete-orphan")
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    if models.storage_t != "db":
        @property
        def cities(self):
            city_list = []
            all_cities = models.storage.all(City)
            
            for city in all_cities.values():
                if city.state_id == self.id:
                    city_list.append(city)

            return city_list

#!/usr/bin/python3
import os
import json


class FileStorage:
    __file_path = "file.json"
    __objects = {}
    
    def all(self, cls=None):
        if cls is not None:
            new_dict = {}
            for key, value in FileStorage.__objects.items():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    new_dict[key] = value
            return new_dict

        return FileStorage.__objects
    
    def new(self, obj):
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        FileStorage.__objects[key] = obj
    
    def save(self):
        obj_dict = {}
        
        for key, value in FileStorage.__objects.items():
            obj_dict[key] = value.to_dict()
        
        with open(FileStorage.__file_path, "w") as file:
            json.dump(obj_dict, file)

    def reload(self):
        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        classes_dict = {"BaseModel": BaseModel,
                        "User": User,
                        "State": State,
                        "City": City,
                        "Amenity": Amenity,
                        "Place": Place,
                        "Review": Review
                        }

        if os.path.exists(FileStorage.__file_path) is True:
            with open(FileStorage.__file_path, "r") as file:
                data = json.load(file)

            for key, value in data.items():
                class_name = value["__class__"]
                clss = classes_dict[class_name]

                instance = clss(**value)

                self.new(instance)

    def delete(self, obj=None):
        if obj is not None:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            if  key in self.__objects:
                del self.__objects[key]

    def close(self):
        self.reload()

    def get(self, cls, id):
        key = "{}.{}".format(cls.__name__, id)
        if key in self.__objects.keys():
            return self.__objects[key]
        
        return None
        
        
    def count(self, cls=None):
        count = 0
        
        if cls:
            for value in self.__objects.values():
                if value.__class__ == cls:
                    count += 1
        else:
            count = len(self.__objects)

        return count
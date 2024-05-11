#!/usr/bin/python3
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from shlex import split

import cmd
from models import storage

dic = {"BaseModel": BaseModel,
        "State": State, "City": City,
        "User": User, "Amenity": Amenity,
        "Place": Place, "Review": Review}


class HBNBCommand(cmd.Cmd):
    prompt = '(hbnb) '

    def do_quit(self, line):
        return True
    
    def do_EOF(self, line):
        print()
        return True
    
    def _key_value(self, argv):
        new_dict = {}
        key = []
        value = []
        for arg in argv:
            if "=" in arg:
                arg = arg.split("=")
                key.append(arg[0])
                arg[1] = arg[1].replace('_', ' ')
                value.append(eval(arg[1]))
        
        for i in range(len(key)):
            new_dict[key[i]] = value[i]

        return new_dict
                
    def do_create(self, line):
        
        if not line:
            print("** class name missing **")
            return
        
        argv = line.split(" ")
        if argv[0] not in HBNBCommand.class_list:
            print("** class doesn't exist **")
        else:
            new_dict = self._key_value(argv[1:])
            my_model = dic[argv[0]](**new_dict)
            print(my_model.id)
            my_model.save()

    def do_show(self, line):
        if not line:
            print("** class name missing **")
            return
        argv = line.split(" ")

        if argv[0] not in HBNBCommand.class_list:
            print("** class doesn't exist **")
        elif len(argv) == 1:
            print("** instance id missing **")
        else:
            all_objects = storage.all()
            
            for key, value in all_objects.items():
                object_name = value.__class__.__name__
                object_id = str(value.id)
                if object_name == argv[0] and object_id == argv[1]:
                    print(value)
                    return
            print("** no instance found **")

    def do_destroy(self, line):
        if not line:
            print("** class name missing **")
            return
        argv = line.split(" ")

        if argv[0] not in HBNBCommand.class_list:
            print("** class doesn't exist **")
        elif len(argv) == 1:
            print("** instance id missing **")
        else:
            all_objects = storage.all()
            del_key = ''

            for key, value in all_objects.items():
                object_name = value.__class__.__name__
                object_id = str(value.id)
                if object_name == argv[0] and object_id == argv[1]:
                    del_key = key

            if del_key:
                del all_objects[del_key]
                storage.save()
                return
            else:
                print("** no instance found **")

    def do_all(self, line):
        if not line:
            print("** class name missing **")
            return

        if line not in HBNBCommand.class_list:
            print("** class doesn't exist **")
        else:
            all_objects = storage.all(dic[line])
            objects = []

            for key, value in all_objects.items():
                object_name = value.__class__.__name__
                if object_name == line:
                    objects += [value.__str__()]
            print(objects)

    def do_update(self, line):
        if not line:
            print("** class name missing **")
            return

        argv = line.split(" ")

        if argv[0] not in HBNBCommand.class_list:
            print("** class doesn't exist **")
        elif len(argv) == 1:
            print("** instance id missing **")
        else:
            all_objects = storage.all()
            for key, value in all_objects.items():
                object_name = value.__class__.__name__
                object_id = value.id

                if argv[0] == object_name and argv[1] == object_id:
                    if len(argv) == 2:
                        print("** attribute name missing **")
                    elif len(argv) == 3:
                        print("** value missing **")
                    else:
                        setattr(value, argv[2], argv[3])
                        storage.save()
                        return
            print("** no instance found **")
            

if __name__ == '__main__':
    HBNBCommand().cmdloop()
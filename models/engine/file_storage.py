#!/usr/bin/python3
""" FileStorage class """


import json
import os.path


class FileStorage:
    """ Defines the FileStorage class.
    
    Class attributes:
        file_path (str): Private. Path to the JSON file
        objects (dict): Private. Stores all objects by <class name>.id
    """
    
    __file_path = "file.json"
    __objects = {}
    
    def all(self, cls=None):
        """ Returns the dict of all objects sorted by <class name>.id
        
        Args:
            cls (str): Optionnal. Class to show the instances of
        """
        if cls is not None:
            objects = {}
            for key, value in self.__objects.items():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    objects[key] = value
            return objects
        return self.__objects
    
    def new(self, obj):
        """ Sets in __objects the obj with his <class name>.id as key
        
        Args:
            obj (<class name>): The new FileStorage object
        """
        attr = f"{type(obj).__name__}.{obj.id}"
        self.__objects[attr] = obj
        
    def save(self):
        """ Serializes __objects to the JSON file """
        json_dict = {}
        for attr, value in self.__objects:
            json_dict[attr] = value.to_dict()
        
        with open(self.__file_path, "w", encoding='utf-8') as f:
            json.dump(json_dict, f)
            
    def reload(self):
        """ Deserializes the JSON file into __objects if it exists """
        from models import base_model, user
        
        modules = {
            "BaseModel": base_model,
            "User": user
        }
        
        if os.path.exists(self.__file_path):
            with open(self.__file_path, "r", encoding='utf-8') as f:
                for attr, value in json.load(f).items():
                    class_name = value['__class__']
                    if class_name in modules:
                        cls = getattr(modules[class_name], class_name)
                        
                    obj = cls(**value)
                    self.__objects[attr] = obj

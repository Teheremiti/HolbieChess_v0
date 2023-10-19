#!/usr/bin/python3
""" BaseModel class """


import uuid
from datetime import datetime
from models import storage


class BaseModel:
    """ Defines the BaseModel class from which any class related to
    user or game information will inherit"""

    def __init__(self, *args):
        """ Constructor method. Initializes an instance's unique id and saves
        the datetime of creation or update
        
        Args:
            *args (tuple): New object's attributes
            **kwargs (dict): Optional. New object's attributes
        """
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        storage.new(self)

    def __str__(self):
        """  Defines a new printing format """
        return "class: {} | id: {} | {}".format(self.__class__.__name__,
                                                self.id, self.__dict__)

    def save(self):
        """ Updates the updated_at attribute to the current datetime """
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """ Returns the __dict__ of the instance """
        new_dict = self.__dict__.copy()

        new_dict['__class__'] = self.__class__.__name__
        new_dict['created_at'] = self.created_at.isoformat()
        new_dict['updated_at'] = self.updated_at.isoformat()

        return new_dict

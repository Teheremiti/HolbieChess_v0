#!/usr/bin/python3
""" User class """


from models.base_model import BaseModel


class User(BaseModel):
    """ Defines the User class.
    
    Attributes:
        first_name (str): User first name
        last_name (str): User las name
        email (str): User email
        password (str): User password
        birthday (str): User birthday. Format DD/MM/YYYY
        gender (str): User gender
    """
    
    first_name = ""
    last_name = ""
    email = ""
    password = ""
    birthday = "DD/MM/YYYY"
    gender = ""

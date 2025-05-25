#!/usr/bin/python3
"""This module defines a class User"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from os import getenv


class User(BaseModel, Base):
    """This class defines a user by various attributes"""

    __tablename__ = "users"

    if getenv("HBNB_TYPE_STORAGE") == "db":
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128))
        last_name = Column(String(128))
        places = relationship(
            "Place", back_populates="user", cascade="all, delete-orphan"
        )
        reviews = relationship(
            "Review", back_populates="user", cascade="all, delete-orphan"
        )
    else:
        # for file storage
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if getenv("HBNB_TYPE_STORAGE") == "db":
            if "email" not in kwargs:
                self.email = ""
            if "password" not in kwargs:
                self.password = ""
            if "first_name" not in kwargs:
                self.first_name = ""
            if "last_name" not in kwargs:
                self.last_name = ""

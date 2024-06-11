#!/usr/bin/env python3
""" User model """
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base


class User(Base):
    """ user class model """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    session = Column(String, nullable=True)
    reset_token = Column(String, nullable=True)

#!/usr/bin/env python3
""" Authentication model """
import bcrypt
from user import User
from db import DB
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """ returns the hased password in bytes """
    salt = bcrypt.gensalt()
    pwd = bcrypt.hashpw(password.encode('utf-8'), salt)
    return pwd


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ registers users into the database """
        try:
            user = self._db.find_user_by(email=email)
        except (NoResultFound, InvalidRequestError):
            pwd = _hash_password(password)
            added_user = self._db.add_user(email, pwd)
            return added_user
        else:
            raise ValueError("User {} already exists".format(email))

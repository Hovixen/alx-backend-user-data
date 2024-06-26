#!/usr/bin/env python3
""" Authentication model """
import bcrypt
import uuid
from user import User
from db import DB
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """ returns the hased password in bytes """
    salt = bcrypt.gensalt()
    pwd = bcrypt.hashpw(password.encode('utf-8'), salt)
    return pwd


def _generate_uuid() -> str:
    """ returns a string of the generated uuid """
    return str(uuid.uuid4())


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

    def valid_login(self, email: str, password: str) -> bool:
        """ validates if the users email matches the password """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'),
                                  user.hashed_password)
        except (NoResultFound, InvalidRequestError):
            return False

    def create_session(self, email: str) -> str:
        """ add session to user and returns the session ID """
        try:
            user = self._db.find_user_by(email=email)
            user.session_id = _generate_uuid()
            return user.session_id
        except (NoResultFound, InvalidRequestError):
            return None

    def get_user_from_session_id(self, session_id: str = None) -> User:
        """ returns corresponding user or None from a session """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except (NoResultFound, InvalidRequestError):
            return None

    def destroy_session(self, user_id: str) -> None:
        """ destroys user session and returns None """
        try:
            user = self._db.find_user_by(id=user_id)
            user.session_id = None
            return None
        except (NoResultFound, InvalidRequestError):
            return None

    def get_reset_password_token(self, email: str) -> str:
        """ generates and updates user reset token """
        try:
            user = self._db.find_user_by(email=email)
            user.reset_token = _generate_uuid()
            return user.reset_token
        except (NoResultFound, InvalidRequestError):
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """ retrieves the corresponding user of the reset_token and update
            users password
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            new_pwd = _hash_password(password)
            user.hashed_password = new_pwd
            user.reset_token = None
            return None
        except (NoResultFound, InvalidRequestError):
            raise ValueError

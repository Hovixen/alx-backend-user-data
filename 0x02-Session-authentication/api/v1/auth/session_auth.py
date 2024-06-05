#!/usr/bin/env python3
""" session authentication """
import uuid
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """ Session authentication class """
    def __init__(self):
        """ initializes the class """
        self.user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ creates sessio id for user """
        if user_id is None or type(user_id) is not str:
            return None
        session_id = uuid.uuid4()
        self.user_id_by_session_id[session_id] = user_id
        return session_id

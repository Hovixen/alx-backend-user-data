#!/usr/bin/env python3
""" Auth Class """
from flask import request
from typing import List, TypeVar


class Auth:
    """ the auth class"""
    def __init__(self):
        """ initializing the class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ function requires auth """
        if path is None:
            return True
        if excluded_paths is None:
            return True
        if not path.endswith('/'):
            path += '/'

        for x_path in excluded_paths:
            if not x_path.endswith('/'):
                x_path += '/'
            if path == x_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """ header authorization function """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ current user function """
        return None

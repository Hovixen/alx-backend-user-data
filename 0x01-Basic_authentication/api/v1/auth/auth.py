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
        return False

    def authorization_header(self, request=None) -> str:
        """ header authorization function """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ current user function """
        return None

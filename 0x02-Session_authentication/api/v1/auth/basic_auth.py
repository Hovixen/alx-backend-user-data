#!/usr/bin/env python3
""" Basic authentication class """
import base64
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """ the basic authentication class """
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """ function returns the authorization header """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        start = len('Basic ')
        return authorization_header[start:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """ function decodes the encoded authorization header """
        if (base64_authorization_header is None or
                not isinstance(base64_authorization_header, str)):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            decoded_string = decoded_bytes.decode("utf-8")
            return decoded_string
        except (base64.binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """ function extracts username and password """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        email, pwd = decoded_base64_authorization_header.split(':', 1)
        return email, pwd

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """ function returns user instance based on email and password """
        if not isinstance(user_email, str):
            return None
        if not isinstance(user_pwd, str):
            return None

        User.load_from_file()
        users = User.search({'email': user_email})
        if users is not None:
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ retrieves the User instance of a request """
        if request is None:
            return None

        header = self.authorization_header(request)
        if header is None:
            return None

        extract = self.extract_base64_authorization_header(header)
        if extract is None:
            return None

        decode = self.decode_base64_authorization_header(extract)
        if decode is None:
            return None

        email, pwd = self.extract_user_credentials(decode)
        if email is None or pwd is None:
            return None

        user = self.user_object_from_credentials(email, pwd)
        if user is None:
            return None

        return user

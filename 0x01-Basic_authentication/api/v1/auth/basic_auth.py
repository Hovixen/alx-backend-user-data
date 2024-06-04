#!/usr/bin/env python3
""" Basic authentication class """
import base64
from api.v1.auth.auth import Auth


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

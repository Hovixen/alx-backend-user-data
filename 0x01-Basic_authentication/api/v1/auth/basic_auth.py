#!/usr/bin/env python3
""" Basic authentication class """
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """ the basic authentication class """
    def extract_base64_authorization_header(self, authorization_header: str
                                            ) -> str:
        """ function returns the authorization header """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        start = len('Basic ')
        return authorization_header[start:]

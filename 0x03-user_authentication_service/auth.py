#!/usr/bin/env python3
""" Authentication model """
import bcrypt


def _hash_password(password: str) -> bytes:
        """ returns the hased password in bytes """
        salt = bcrypt.gensalt()
        pwd = bcrypt.hashpw(password.encode('utf-8'), salt)
        return pwd

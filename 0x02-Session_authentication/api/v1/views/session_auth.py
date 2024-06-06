#!/usr/bin/env python3
""" handles all routes for session authentication """
from . import app_views
from flask import abort, jsonify, request
from models.user import User
from typing import Any, Dict


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login_user() -> Any[str, Dict[str]]:
    """ logs in a user and creates a cookie session for the user """
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None:
        return jsonify({'error': 'email missing'}), 401
    if password is None:
        return jsonify({'error': 'password missing'}), 401
    User.load_from_file()
    users = User.search({'email': email})
    for user in users:
        if user.is_valid_password(password):
            from api.v1.app import auth




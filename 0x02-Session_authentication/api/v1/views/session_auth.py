#!/usr/bin/env python3
""" handles all routes for session authentication """
import os
from . import app_views
from flask import abort, jsonify, request
from models.user import User
# from typing import Any, Dict


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login_user():
    """ logs in a user and creates a cookie session for the user """
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None:
        return jsonify({'error': 'email missing'}), 400
    if password is None:
        return jsonify({'error': 'password missing'}), 400
    User.load_from_file()
    users = User.search({'email': email})
    try:
        for user in users:
            if user.is_valid_password(password):
                from api.v1.app import auth
                session_id = auth.create_session(user.id)
                session_name = os.getenv("SESSION_NAME")
                res = jsonify(user.to_json())
                res.set_cookie(session_name, session_id)
                return res
            return jsonify({'error': 'wrong password'}), 401
    except Exception:
        return jsonify({'error': 'no user found for this email'}), 404
    if not users:
        return jsonify({'error': 'no user found for this email'}), 404

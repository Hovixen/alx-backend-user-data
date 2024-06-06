#!/usr/bin/env python3
""" handles all routes for session authentication """
import os
from . import app_views
from flask import abort, jsonify, request
from models.user import User

@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login_user():
    """ logs in a user and creates a cookie session for the user """
    email = request.form.get('email')
    password = request.form.get('password')
    
    if not email:
        return jsonify({'error': 'email missing'}), 400
    if not password:
        return jsonify({'error': 'password missing'}), 400
    
    try:
        users = User.search({'email': email})
    except Exception:
        return jsonify({'error': 'no user found for this email'}), 404
    
    if not users:
        return jsonify({'error': 'no user found for this email'}), 404
    
    user = users[0]
    
    if not user.is_valid_password(password):
        return jsonify({'error': 'wrong password'}), 401
    
    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    session_name = os.getenv("SESSION_NAME")
    res = jsonify(user.to_json())
    res.set_cookie(session_name, session_id)
    
    return res

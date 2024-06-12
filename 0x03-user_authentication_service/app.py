#!/usr/bin/env python3
""" The Application """
from flask import Flask, jsonify, request, abort, url_for, redirect
from auth import Auth


AUTH = Auth()
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def index():
    """ default index """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """ route registers users """
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """ creates new session for the user and store it as a cookie """
    email = request.form.get('email')
    password = request.form.get('password')

    if AUTH.valid_login(email, password):
        res = jsonify({"email": email, "message": "logged in"})
        session_id = AUTH.create_session(email)
        res.set_cookie("session_id", session_id)
        return res
    else:
        abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """ logs out user by deleting user session ID """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect(url_for(index))
    else:
        abort(403)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')

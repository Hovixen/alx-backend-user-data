#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None
auth_inst = getenv("AUTH_TYPE")

if auth_inst:
    if auth_inst == "auth":
        from api.v1.auth.auth import Auth
        auth = Auth()

    elif auth_inst == "basic_auth":
        from api.v1.auth.basic_auth import BasicAuth
        auth = BasicAuth()

    elif auth_inst == "session_auth":
        from api.v1.auth.session_auth import SessionAuth
        auth = SessionAuth()
    elif AUTH_TYPE == "session_exp_auth":
        from api.v1.auth.session_exp_auth import SessionExpAuth
        auth = SessionExpAuth()
    elif AUTH_TYPE == "session_db_auth":
        from api.v1.auth.session_db_auth import SessionDBAuth
        auth = SessionDBAuth()


@app.before_request
def before_request():
    """ funciton is executed before the routes function """
    if auth is None:
        return
    excluded_path = ["/api/v1/status/", "/api/v1/unauthorized",
                     "/api/v1/forbidden", "/api/v1/auth_session/login/"]
    if not auth.require_auth(request.path, excluded_path):
        return
    if auth.authorization_header(request) is None \
            and auth.session_cookie(request) is None:
        raise abort(401)
    if auth.current_user(request) is None:
        raise abort(403)
    request.current_user = auth.current_user(request)


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """ unauthorized handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """ forbidden handler
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port, debug=True)

#!/usr/bin/env python3
""" Module of Session Authentication Views
"""
from api.v1.views import app_views
from flask import jsonify, request
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> str:
    """ POST /api/v1/auth_session/login
    Return:
      - list of all User objects JSON represented
    """
    email = request.form.get("email")
    password = request.form.get("password")
    if not email or email == '':
        return jsonify({"error": "email missing"}), 400
    if not password or password == '':
        return jsonify({"error": "password missing"}), 400
    try:
        users = User.search({"email": email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404
    if len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    user = users[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    # We import the `auth` variable to create a session for our user
    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    response = jsonify(user.to_json())
    response.set_cookie("{}={}".format(getenv("SESSION_NAME"), session_id))
    return response

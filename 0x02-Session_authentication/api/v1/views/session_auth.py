#!/usr/bin/env python3
"""Module for session
"""
from flask import jsonify, request, abort

from typing import Tuple

import os

from api.v1.views import app_views

from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> Tuple[str, int]:
    """session routes

    Returns:
        str: _description_
    """
    email = request.form.get('email')
    password = request.form.get('password')
    not_found = {'error': 'no user found for this email'}

    if email is None or len(email.strip()) == 0:
        return jsonify({"error": "email missing"}), 400
    if password is None or len(password.strip()) == 0:
        return jsonify({"error": "password missing"}), 400
    try:
        users = User.search({'email': email})
    except Exception:
        return jsonify(not_found), 400
    if len(users) <= 0:
        return jsonify(not_found), 400
    if users[0].is_valid_password(password):
        from api.v1.app import auth
        session_id = auth.create_session(getattr(users[0], 'id'))
        resp = jsonify(users[0].to_json())
        resp.set_cookie(os.getenv("SESSION_NAME"), session_id)
        return resp
    return jsonify({"error": "wrong password"}), 401

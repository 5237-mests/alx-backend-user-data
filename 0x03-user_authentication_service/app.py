#!/usr/bin/env python3
"""flask app
"""
from flask import Flask, jsonify, request, abort, redirect
from sqlalchemy.orm.exc import NoResultFound

from auth import Auth

AUTH = Auth()


app = Flask(__name__)


@app.route("/", methods=['GET'])
def index():
    """index"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'], strict_slashes=False)
def users():
    """route user"""
    password = request.form.get("password")
    email = request.form.get("email")
    try:
        AUTH._db.find_user_by(email=email)
    except NoResultFound:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=['POST'], strict_slashes=False)
def login():
    """login user"""
    password = request.form.get("password")
    email = request.form.get("email")
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie("session_id", session_id)
        return response
    else:
        abort(401)


@app.route("/sessions", methods=['DELETE'], strict_slashes=False)
def logout():
    """log out user"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")

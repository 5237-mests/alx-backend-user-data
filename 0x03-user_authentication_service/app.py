#!/usr/bin/env python3
"""flask app
"""
from flask import Flask, jsonify, request
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")

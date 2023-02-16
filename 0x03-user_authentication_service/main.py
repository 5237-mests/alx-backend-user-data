#!/usr/bin/env python3
"""main module
"""
import requests

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

base_url = "http://localhost:5000/"


def register_user(email: str, password: str) -> None:
    """test register"""
    body = {'email': email, 'pasword': password}
    resp = requests.post(f"{base_url}users", data=body)
    assert resp.status_code == 200
    assert resp.json() == {"email": email, "message": "user created"}
    resp = requests.post(f"{base_url}users", data=body)
    assert resp.status_code == 400
    assert resp.json() == {"message": "email already registere5d"}


def log_in_wrong_password(email: str, password: str) -> None:
    """test wrong login attempt"""
    body = {'email': email, 'pasword': password}
    resp = requests.post(f"{base_url}sessions", data=body)
    assert resp.status_code == 401


def log_in(email: str, password: str) -> str:
    """test wright login"""
    body = {'email': email, 'pasword': password}
    resp = requests.post(f"{base_url}sessions", data=body)
    assert resp.status_code == 200
    assert resp.json() == {"email": email, "message": "logged in"}
    return resp.cookies.get('session_id')


def profile_unlogged() -> None:
    """test unlogged profile"""
    resp = requests.get(f"{base_url}profile")
    assert resp.status_code == 403


def profile_logged(session_id: str) -> None:
    """test logged user"""
    req_cookies = {'session_id': session_id}
    resp = requests.get(f"{base_url}profile", cookies=req_cookies)
    assert resp.status_code == 200
    assert 'email' in resp.json()


def log_out(session_id: str) -> None:
    """test logout"""
    req_cookies = {'session_id': session_id}
    resp = requests.delete(f"{base_url}profile", cookies=req_cookies)
    assert resp.status_code == 200
    assert resp.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """test reseting psw"""
    body = {'email': email}
    resp = requests.post(f"{base_url}reset_password", data=body)
    assert resp.status_code == 200
    assert "email" in resp.json()
    assert resp.json()["email"] == email
    assert "reset_token" in resp.json()
    return resp.json().get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """test update psw"""
    body = {
        'email': email,
        'reset_token': reset_token,
        'new_password': new_password,
    }
    resp = requests.put(f"{base_url}reset_password", data=body)
    assert resp.status_code == 200
    assert resp.json() == {"email": email, "message": "Password updated"}


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)

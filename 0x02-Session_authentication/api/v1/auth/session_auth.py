#!/usr/bin/env python3
"""Session module
"""
import uuid

from api.v1.auth.auth import Auth

from models.user import User


class SessionAuth(Auth):
    """Session class
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """creates a Session ID for a user_id:

        Args:
            user_id (str, optional): user id. Defaults to None.

        Returns:
            str: Session ID
        """
        if type(user_id) == str:
            session_id = str(uuid.uuid4())
            self.user_id_by_session_id[session_id] = user_id
            return session_id
        return None

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """creates Session ID:

        Args:
            session_id (str, optional): session id. Defaults to None.

        Returns:
            str: returns a User ID based on a Session ID:
        """
        if type(session_id) is str:
            return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> User:
        """cookie

        Args:
            request (_type_, optional): _description_. Defaults to None.
        """
        cookie_value = self.session_cookie(request)
        user_id = self.user_id_for_session_id(cookie_value)
        return User.get(user_id)

    def destroy_session(self, request=None):
        """logout or deletes the session

        Args:
            request (_type_, optional): _description_. Defaults to None.
        """
        session_id = self.session_cookie(request)
        user_id_for_session_id = self.user_id_for_session_id(session_id)
        if (request is None or session_id is None) or \
                user_id_for_session_id is None:
            return False
        if session_id in self.user_id_by_session_id:
            del self.user_id_by_session_id[session_id]
        return True

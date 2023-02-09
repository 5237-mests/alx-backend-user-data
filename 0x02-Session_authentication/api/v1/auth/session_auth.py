#!/usr/bin/env python3
"""Session module
"""
from api.v1.auth.auth import Auth

import uuid


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
            ID = str(uuid.uuid4())
            self.user_id_by_session_id[ID] = user_id
            return ID
        return None

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """creates Session ID:

        Args:
            session_id (str, optional): session id. Defaults to None.

        Returns:
            str: returns a User ID based on a Session ID:
        """
        if type(session_id) == str:
            return self.user_id_by_session_id.get(session_id)
        return None

#!/usr/bin/env python3
"""session exp module
"""
from datetime import datetime, timedelta

from os import getenv

from flask import request

from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """Expire Session Id class
    """
    def __init__(self) -> None:
        """Initialize class"""
        super().__init__()
        try:
            self.session_duration = int(getenv('SESSION_DURATION'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """create session method
        """
        try:
            session_Id = super().create_session(user_id)
        except Exception:
            return None
        self.user_id_by_session_id[session_Id] = {
            'user_id': user_id,
            'created_at': datetime.now(),
        }
        return session_Id

    def user_id_for_session_id(self, session_id=None):
        """session id
        """
        if session_id in self.user_id_by_session_id:
            session_dict = self.user_id_by_session_id.get(session_id)
            if self.session_duration <= 0:
                return session_dict.get('user_id')
            if 'created_at' not in session_dict:
                return None
            current_time = datetime.now()
            time_span = timedelta(seconds=self.session_duration)
            exp_time = session_dict['created_at'] + time_span
            if exp_time < current_time:
                return None
            return session_dict.get('user_id')

#!/usr/bin/env python3
"""Module for session db
"""
from models.base import Base


class UserSession(Base):
    """class for creating db
    """
    def __init__(self, *args: list, **kwargs: dict):
        """initialize"""
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')

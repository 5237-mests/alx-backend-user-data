#!/usr/bin/env python3
"""Auth module
"""
from flask import request

from typing import List, TypeVar

import re


class Auth:
    """class Auth
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """_summary_

        Args:
            path (str): _description_
            excluded_paths (List[str]): _description_

        Returns:
            bool: _description_
        """
        if path is not None and excluded_paths is not None:
            for ex_path in map(lambda el: el.strip(), excluded_paths):
                path_pattern = ''
                if ex_path[-1] == '*':
                    path_pattern = '{}.*'.format(ex_path[0:-1])
                elif ex_path[-1] == '/':
                    path_pattern = '{}/*'.format(ex_path[0:-1])
                else:
                    path_pattern = '{}/*'.format(ex_path)
                if re.match(path_pattern, path):
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """_summary_

        Args:
            request (_type_, optional): _description_. Defaults to None.

        Returns:
            str: _description_
        """
        if request is not None:
            return request.headers.get('Authorization', None)
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """_summary_
        """
        return None

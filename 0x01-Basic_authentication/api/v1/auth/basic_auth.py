#!/usr/bin/env python3
"""basic auth module
"""
import re

import base64

from typing import Tuple, TypeVar

from api.v1.auth.auth import Auth

from models.user import User


class BasicAuth(Auth):
    """Class BasicAuth
    """
    def extract_base64_authorization_header(
                                            self,
                                            authorization_header: str
                                            ) -> str:
        """extract base64

        Args:
            authorization_header (str): header

        Returns:
            str: Base64 part of the Authorization header
        """
        if authorization_header is None or \
                type(authorization_header) != str or \
                re.search('Basic ', authorization_header) is None:
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
                                           self,
                                           base64_authorization_header: str
                                           ) -> str:
        """decoder function

        Args:
            base64_authorization_header (str): given

        Returns:
            str: return decoded value
        """
        if base64_authorization_header is None or \
                type(base64_authorization_header) != str:
            return None
        try:
            decoded = base64.b64decode(base64_authorization_header)
            return decoded.decode("utf-8")
        except Exception:
            return None

    def extract_user_credentials(
                                self,
                                decoded_base64_authorization_header: str
                                ) -> Tuple[str, str]:
        """extract cred

        Args:
            decoded_base64_authorization_header (str): decoded cred

        Returns:
            Tuple[str, str]: user and emial.
        """
        if decoded_base64_authorization_header is None or \
                type(decoded_base64_authorization_header) != str or \
                re.search(":", decoded_base64_authorization_header) is None:
            return (None, None)
        splited_string = decoded_base64_authorization_header.split(":")
        email = splited_string[0]
        password = splited_string[1]
        return (email, password)

    def user_object_from_credentials(
                                     self,
                                     user_email: str,
                                     user_pwd: str
                                     ) -> TypeVar('User'):
        """user object
        """
        if type(user_email) == str and type(user_pwd) == str:
            try:
                new_user = User.search({'email': user_email})
            except Exception:
                return None
            if len(new_user) <= 0:
                return None
            if new_user[0].is_valid_password(user_pwd):
                return new_user[0]
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """current user
        """
        auth_h = self.authorization_header(request)
        extract_h = self.extract_base64_authorization_header(auth_h)
        dec_h = self.decode_base64_authorization_header(extract_h)
        email, password = self.extract_user_credentials(dec_h)
        return self.user_object_from_credentials(email, password)

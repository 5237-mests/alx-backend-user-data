#!/usr/bin/env python3
"""basic auth module
"""
import re

import base64

from typing import Tuple

from api.v1.auth.auth import Auth


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
        except Exception:
            return None
        return decoded.decode("utf-8")

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

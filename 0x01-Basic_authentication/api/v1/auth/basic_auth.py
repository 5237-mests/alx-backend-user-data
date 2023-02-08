#!/usr/bin/env python3
"""basic auth module
"""
import re

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

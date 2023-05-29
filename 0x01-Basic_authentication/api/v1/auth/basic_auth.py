#!/usr/bin/env python3
"""Module of Basic Auth
"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """ Basic Authentication Class
    """
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """ Method that extracts the Base64 part of the `Authorization` header
        Returns:
          - None if `authorization_header` is None
          - None if `authorization_header` is not a string
          - None if `authorization_header` doesn’t start by `Basic`
            (with a space at the end)
          - Otherwise, return the value after `Basic` (after the space)
        Assumption:
          - `authorization_header` contains only one `Basic`
        """
        if not authorization_header or type(authorization_header) != str:
            return None
        words = authorization_header.split()
        if words[0] != "Basic":
            return None
        return words[1]

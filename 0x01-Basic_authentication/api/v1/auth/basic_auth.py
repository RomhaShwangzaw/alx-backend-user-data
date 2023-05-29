#!/usr/bin/env python3
"""Module of Basic Auth
"""
from api.v1.auth.auth import Auth
import base64


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
        if not authorization_header.startswith("Basic "):
            return None
        words = authorization_header.split()
        return words[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """ Method that decodes a Base64 string
        Returns:
          - None if `base64_authorization_header` is None
          - None if `base64_authorization_header` is not a string
          - None if `base64_authorization_header` is not a valid Base64
          - Otherwise, return the decoded value as UTF8 string
        """
        if not base64_authorization_header or type(
                base64_authorization_header) != str:
            return None

        try:
            return base64.b64decode(
                base64_authorization_header).decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str) -> (str, str):
        """ Retrieves the user email and password from the Base64 decoded value
        Returns:
          - None, None if decoded_base64_authorization_header is None
          - None, None if decoded_base64_authorization_header is not a string
          - None, None if decoded_base64_authorization_header doesn’t contain :
          - Otherwise, return the user email and the user password
        Assumption:
          - decoded_base64_authorization_header will contain only one :
        """
        if not decoded_base64_authorization_header or type(
                decoded_base64_authorization_header) != str:
            return None, None
        if ":" not in decoded_base64_authorization_header:
            return None, None
        return tuple(decoded_base64_authorization_header.split(":"))

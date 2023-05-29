#!/usr/bin/env python3
"""Module of Basic Auth
"""
from api.v1.auth.auth import Auth
import base64
from models.user import User
from typing import TypeVar


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
        return tuple(decoded_base64_authorization_header.split(":", 1))

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """ Retrieves the User instance based on his email and password
        Returns:
          - None if `user_email` is None or not a string
          - None if `user_pwd` is None or not a string
          - None if the database (file) doesn’t contain any
            User instance with email equal to `user_email`
          - None if `user_pwd` is not the password of the User instance found
          - Otherwise, return the User instance
        """
        if not user_email or type(user_email) != str:
            return None
        if not user_pwd or type(user_pwd) != str:
            return None
        users = User.search({"email": user_email})
        if len(users) == 0:
            return None
        user = users[0]
        if not user.is_valid_password(user_pwd):
            return None
        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """ Retrieves the User instance for a request
        """
        auth_header = self.authorization_header(request)
        b64_auth_header = self.extract_base64_authorization_header(auth_header)
        decoded_hdr = self.decode_base64_authorization_header(b64_auth_header)
        email, pwd = self.extract_user_credentials(decoded_hdr)
        user = self.user_object_from_credentials(email, pwd)
        return user

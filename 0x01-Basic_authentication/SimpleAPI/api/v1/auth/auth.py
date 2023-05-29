#!/usr/bin/env python3
"""Module of API Authentication
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """ Authentication Class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Method that authenticates users
        """
        return False

    def authorization_header(self, request=None) -> str:
        """ Method that adds authorization credentials to request header
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Method that returns the current user
        """
        return None

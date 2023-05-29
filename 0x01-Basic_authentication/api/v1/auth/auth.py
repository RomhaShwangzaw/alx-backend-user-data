#!/usr/bin/env python3
"""Module of API Authentication
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """ Authentication Class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Method that defines which routes don't need authentication
        Return:
          - True if `path` is None
          - True if `excluded_paths` is None or empty
          - False if `path` is in `excluded_paths`
        Assumptions:
          - `excluded_paths` contains string path always ending by a /
          - method is slash tolerant: path=/api/v1/status and
            path=/api/v1/status/ must be returned False if
            `excluded_paths` contains /api/v1/status/
        """
        if not path or not excluded_paths or len(excluded_paths) == 0:
            return True
        if any(path in x for x in excluded_paths):
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """ Method that adds authorization credentials to request header
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Method that returns the current user
        """
        return None

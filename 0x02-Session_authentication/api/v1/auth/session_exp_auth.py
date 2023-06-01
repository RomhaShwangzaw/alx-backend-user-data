#!/usr/bin/env python3
""" Module of Session Expiry Authentication
"""
from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """ Session Expiry Authentication class
    """
    def __init__(self):
        """ Initializer method
        """
        super().__init__()
        try:
            self.session_duration = int(getenv("SESSION_DURATION"))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id: str = None) -> str:
        """ Creates a Session ID for a `user_id`
        Return:
          - None if `user_id` is None
          - None if `user_id` is not a string
          - Otherwise, return the Session ID
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        session_dict = {'user_id': user_id,
                        'created_at': datetime.now()}
        self.user_id_by_session_id[session_id] = session_dict
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Retrieves a User ID based on a Session ID
        Return:
          - None if `session_id` is None
          - None if `session_id` is not a string
          - None if `user_id_by_session_id` doesn’t contain
            any key equals to `session_id`
          - the `user_id` key from the session dictionary if
            `self.session_duration` is equal or under 0
          - None if session dictionary doesn’t contain a key `created_at`
          - None if the `created_at` + session_duration seconds
            are before the current datetime
          - Otherwise, return `user_id` from the session dictionary
        """
        if not session_id or type(session_id) != str:
            return None
        session_dict = self.user_id_by_session_id.get(session_id)
        if not session_dict:
            return None
        if self.session_duration <= 0:
            return session_dict.get('user_id')
        created_at = session_dict.get('created_at')
        if not created_at:
            return None
        if created_at + timedelta(
                seconds=self.session_duration) < datetime.now():
            return None
        return session_dict.get('user_id')

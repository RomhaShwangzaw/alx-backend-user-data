#!/usr/bin/env python3
""" Module of Session Authentication
"""
from api.v1.auth.auth import Auth
from models.user import User
import uuid


class SessionAuth(Auth):
    """ Session Authentication class
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Creates a Session ID for a `user_id`
        Return:
          - None if `user_id` is None
          - None if `user_id` is not a string
          - Otherwise, return the Session ID
        """
        if not user_id or type(user_id) != str:
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Retrieves a User ID based on a Session ID
        Return:
          - None if `session_id` is None
          - None if `session_id` is not a string
          - The value (the User ID) for the key `session_id`
            in the dictionary `user_id_by_session_id`
        """
        if not session_id or type(session_id) != str:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """ Returns a User instance based on a cookie value
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        return User.get(user_id)

    def destroy_session(self, request=None):
        """ Deletes the user session / logout
        Return:
          - False if the request is equal to None
          - False if the request doesn’t contain the Session ID cookie
          - False if the Session ID of the request is not linked to any User ID
          - Otherwise, delete in self.user_id_by_session_id the Session ID
            (as key of this dictionary) and return True
        """
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return False
        del self.user_id_by_session_id[session_id]
        return True

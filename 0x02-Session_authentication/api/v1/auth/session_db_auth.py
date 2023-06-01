#!/usr/bin/env python3
""" Module of Session DB Authentication
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """ Session DB Authentication class
    """
    def create_session(self, user_id: str = None) -> str:
        """ Creates and stores new instance of UserSession
        Return:
          - None if `user_id` is None
          - None if `user_id` is not a string
          - Otherwise, return the Session ID
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Retrieves a User ID from a database based on a Session ID
        Return:
          - None if `session_id` is None
          - None if `session_id` is not a string
          - Otherwise, return `user_id` from the UserSession instance
        """
        user_id = super().user_id_for_session_id(session_id)
        if not user_id:
            return None
        try:
            user_sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return None
        if len(user_sessions) == 0:
            return None
        user_session = user_sessions[0]
        return user_session.user_id

    def destroy_session(self, request=None):
        """ Destroys the UserSession based on the Session ID
        from the request cookie

        Return:
          - False if the request is equal to None
          - False if the request doesn’t contain the Session ID cookie
          - False if the Session ID of the request is not linked
            to any UserSession instance
          - Otherwise, delete the UserSession instance and return True
        """
        status = super().destroy_session(request)
        if not status:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        try:
            user_sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return False
        if len(user_sessions) == 0:
            return False
        user_session = user_sessions[0]
        user_session.remove()
        return True

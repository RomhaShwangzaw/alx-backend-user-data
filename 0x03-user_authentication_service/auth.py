#!/usr/bin/env python3
""" Authentication Module
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """ Hashes a password and returns the salted hash of the password
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

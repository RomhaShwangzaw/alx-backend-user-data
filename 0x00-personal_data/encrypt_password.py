#!/usr/bin/env python3
"""Password Encryption Module"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    Encrypts or hashes a password and
    returns the hashed password.
    """
    pwd = bytes(password, "utf-8")
    hashed = bcrypt.hashpw(pwd, bcrypt.gensalt())
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Checks if the provided password matches the hashed password
    Return:
    `True` if the passwords match
    `False` if the passwords don't match
    """
    pwd = bytes(password, "utf-8")
    return bcrypt.checkpw(pwd, hashed_password)

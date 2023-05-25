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

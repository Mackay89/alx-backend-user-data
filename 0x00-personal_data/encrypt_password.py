#!/usr/bin/env python3
"""Module for encrypting passwords.
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes the provided password using bcrypt.

    Args:
        password (str): Password to be hashed.

    Returns:
        bytes: A salted, hashed password in byte string format.
    """
    # Salt and hash the password using the bcrypt package
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Validates that the provided password matches the hashed password.

    Args:
        hashed_password (bytes): Hashed password.
        password (str): Password to be validated.

    Returns:
        bool: True if the hashed password was formed from the given password,
        otherwise False.
    """
    # Match the hashed password with the given password
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)


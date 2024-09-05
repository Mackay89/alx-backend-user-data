#!/usr/bin/env python3
"""User module"""
import bcrypt
from models.base import Base


class User(Base):
    """User class"""

    def __init__(self, *args: list, **kwargs: dict):
        """Initialize a User instance"""
        super().__init__(*args, **kwargs)
        self.email = kwargs.get('email')
        self._password = kwargs.get('_password')
        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')

    @property
    def password(self) -> str:
        """Getter for the password"""
        return self._password

    @password.setter
    def password(self, pwd: str):
        """Setter for a new password: encrypt using bcrypt"""
        if pwd and isinstance(pwd, str):
            salt = bcrypt.gensalt()
            self._password = bcrypt.hashpw(pwd.encode(), salt).decode()
        else:
            self._password = None

    def is_valid_password(self, pwd: str) -> bool:
        """Validate a password"""
        if pwd and isinstance(pwd, str) and self.password:
            return bcrypt.checkpw(pwd.encode(), self.password.encode())
        return False

    def display_name(self) -> str:
        """Display user name based on email/first_name/last_name"""
        if not self.first_name and not self.last_name:
            return self.email if self.email else ""
        return f"{self.first_name or ''} {self.last_name or ''}".strip()

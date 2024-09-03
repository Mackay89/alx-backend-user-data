#!/usr/bin/env python3
"""User module."""

import hashlib
from models.base import Base

class User(Base):
    """User class with methods to handle user data."""

    def __init__(self, *args: list, **kwargs: dict):
        """Initialize a User instance."""
        super().__init__(*args, **kwargs)
        self.email = kwargs.get('email')
        self._password = kwargs.get('_password')
        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')

    @property
    def password(self) -> str:
        """Getter of the password."""
        return self._password

    @password.setter
    def password(self, pwd: str):
        """Setter of a new password: encrypt in SHA256."""
        if isinstance(pwd, str) and pwd:
            self._password = hashlib.sha256(pwd.encode()).hexdigest().lower()
        else:
            self._password = None

    def is_valid_password(self, pwd: str) -> bool:
        """Validate a password."""
        if not isinstance(pwd, str):
            return False
        return self._password is not None and hashlib.sha256(pwd.encode()).hexdigest().lower() == self._password

    def display_name(self) -> str:
        """Display User name based on email, first_name, and last_name."""
        if self.email:
            if self.first_name and self.last_name:
                return f"{self.first_name} {self.last_name}"
            elif self.first_name:
                return self.first_name
            elif self.last_name:
                return self.last_name
            else:
                return self.email
        return ""


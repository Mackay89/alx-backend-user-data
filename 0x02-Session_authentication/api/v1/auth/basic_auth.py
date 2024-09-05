#!/usr/bin/env python3
"""Module for basic authentication
"""
import base64
import binascii
from typing import Tuple, TypeVar, Optional

from models.user import User
from .auth import Auth


class BasicAuth(Auth):
    """Basic authentication class."""

    def extract_base64_authorization_header(
            self, authorization_header: str) -> Optional[str]:
        """
        Extracts the Base64 part of the Authorization header.

        Args:
            authorization_header (str): The Authorization header string.

        Returns:
            Optional[str]: The Base64 part of the Authorization header, or None
            if the header is invalid.
        """
        if authorization_header is None or not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split("Basic ")[1].strip()

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> Optional[str]:
        """
        Decodes the Base64 string `base64_authorization_header` and
        returns the decoded value as a UTF8 string.

        Args:
            base64_authorization_header (str): A Base64 encoded string to be
            decoded.

        Returns:
            Optional[str]: The decoded value as a UTF8 string, or None if the
            input is invalid.
        """
        if base64_authorization_header is None or not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded = base64.b64decode(base64_authorization_header, validate=True)
            return decoded.decode('utf-8')
        except (binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(self, decoded_header: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Extracts the user email and password from the decoded header string.

        Args:
            decoded_header (str): A decoded header string.

        Returns:
            Tuple[Optional[str], Optional[str]]: A tuple containing the user email
            and password, or (None, None) if the input is invalid.
        """
        if decoded_header is None or not isinstance(decoded_header, str):
            return None, None
        try:
            email, password = decoded_header.split(':', 1)
            return email, password
        except ValueError:
            return None, None

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> Optional[TypeVar('User')]:
        """
        Returns the User instance based on the email and password.

        Args:
            user_email (str): The user's email.
            user_pwd (str): The user's password.

        Returns:
            Optional[TypeVar('User')]: The User instance or None if the user
            is not found or the password is invalid.
        """
        if not isinstance(user_email, str) or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({'email': user_email})
        except Exception:
            return None
        if not users:
            return None
        user = users[0]
        if not user.is_valid_password(user_pwd):
            return None
        return user

    def current_user(self, request=None) -> Optional[TypeVar('User')]:
        """
        Retrieves the User instance for a request.

        Args:
            request (:obj:`flask.Request`, optional): The request object. Defaults to None.

        Returns:
            Optional[TypeVar('User')]: The User instance based on the request,
            or None if the authentication fails.
        """
        auth_header = self.authorization_header(request)
        b64_auth_header = self.extract_base64_authorization_header(auth_header)
        dec_header = self.decode_base64_authorization_header(b64_auth_header)
        user_email, user_pwd = self.extract_user_credentials(dec_header)
        return self.user_object_from_credentials(user_email, user_pwd)

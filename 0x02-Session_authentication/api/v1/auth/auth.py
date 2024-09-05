#!/usr/bin/env python3
"""
Module for authentication
"""
import os
from typing import List, Optional

from flask import request


class Auth:
    """Template for all authentication systems implemented in this app."""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines if authentication is required for a given path.

        Args:
            path (str): The path to check against the list of excluded paths.
            excluded_paths (List[str]): The list of excluded paths.

        Returns:
            bool: True if the path is not in the excluded paths
            list, False otherwise.
        """
        if not path:
            return True
        if not excluded_paths:
            return True

        # Normalize path by removing trailing slash
        path = path.rstrip('/')

        for excluded_path in excluded_paths:
            # Handle wildcard paths (e.g., '/api/v1/*')
            if (excluded_path.endswith('*') and
                path.startswith(excluded_path[:-1])):
                return False
            # Handle exact matches
            if path == excluded_path.rstrip('/'):
                return False

        return True

    def authorization_header(self, request=None) -> Optional[str]:
        """
        Retrieves the Authorization header from a request.

        Args:
            request (Optional[flask.Request]): The request
            object. Defaults to None.

        Returns:
            Optional[str]: The value of the Authorization header, or None if not present.
        """
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> Optional['User']:
        """
        Identifies the current user from the request.

        Args:
            request (Optional[flask.Request]): The request
            object. Defaults to None.

        Returns:
            Optional[User]: The current user. None for now,
            to be implemented later.
        """
        return None

    def session_cookie(self, request=None) -> Optional[str]:
        """
        Retrieves the session cookie from a request.

        Args:
            request (Optional[flask.Request]): The request
            object. Defaults to None.

        Returns:
            Optional[str]: The value of the session cookie, or None if not present.
        """
        if request is None:
            return None

        cookie_name = os.getenv('SESSION_NAME', 'session_id')
        return request.cookies.get(cookie_name)

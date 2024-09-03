#!/usr/bin/env python3
"""
Module for authentication
"""

from typing import List, TypeVar
from flask import request


class Auth:
    """Template for all authentication systems implemented in this app.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Determines if a given path requires authentication.

        Returns True if `path` is None or if `excluded_paths` is None or empty.
        Returns False if `path` is in `excluded_paths`.
        This method is slash-tolerant: paths with or without a trailing slash
        are treated as equivalent.

        Args:
            path (str): The path to check against the list of excluded paths.
            excluded_paths (List[str]): The list of excluded paths.

        Returns:
            bool: True if the path is not in the excluded paths list,
                  False otherwise.
        """
        if not path:
            return True
        if not excluded_paths:
            return True

        # Normalize the path by removing the trailing slash
        path = path.rstrip('/')

        for excluded_path in excluded_paths:
            # Handle wildcard paths
            if excluded_path.endswith('*'):
                if path.startswith(excluded_path[:-1]):
                    return False
            # Handle exact matches, considering trailing slashes
            elif path == excluded_path.rstrip('/'):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """Gets the value of the Authorization header from the request.

        Args:
            request (request, optional): Flask request object.
            Defaults to None.

        Returns:
            str: The value of the Authorization header or None if not present.
        """
        if request is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """Placeholder for retrieving the current user based on the request.

        Args:
            request (request, optional): Flask request object.
            Defaults to None.

        Returns:
            TypeVar('User'): The current user, or None if not implemented.
        """
        return None

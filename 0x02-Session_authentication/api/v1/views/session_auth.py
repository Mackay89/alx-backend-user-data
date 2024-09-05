#!/usr/bin/env python3
"""Module for session authentication views.
"""

import os
from typing import Tuple
from flask import abort, jsonify, request
from api.v1.app import auth
from api.v1.views import app_views
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_auth_login() -> Tuple[str, int]:
    """POST /api/v1/auth_session/login

    Handles the user login and session creation.

    Returns:
        Tuple[str, int]: JSON representation of the authenticated User
        object with a status code.
    """
    # Get the email and password from the request form data
    email = request.form.get('email')
    password = request.form.get('password')

    # Validate email and password
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    # Search for the user by email
    user = User.search({'email': email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404

    # Check if the password is valid
    if not user[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    # Create a session ID for the user
    session_id = auth.create_session(user[0].id)

    # Create a response with the user data in JSON format
    response = jsonify(user[0].to_json())

    # Set the session ID in the cookie
    response.set_cookie(
        os.getenv("SESSION_NAME"),
        session_id
    )

    return response, 200


@app_views.route
('/auth_session/logout', methods=['DELETE'], strict_slashes=False)


def session_auth_logout() -> Tuple[str, int]:
    """DELETE /api/v1/auth_session/logout

    Handles the user logout and session destruction.

    Returns:
        Tuple[str, int]: An empty JSON object with a status code.
    """
    # Destroy the session
    if not auth.destroy_session(request):
        abort(404)

    return jsonify({}), 200

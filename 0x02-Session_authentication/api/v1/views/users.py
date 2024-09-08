#!/usr/bin/env python3
"""Module for User views
Handles operations related to the User model, including:
- Viewing all users
- Viewing a specific user
- Creating a new user
- Deleting a user
- Updating user details
"""

from flask import abort, jsonify, request
from api.v1.views import app_views
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def view_all_users() -> str:
    """GET /api/v1/users
    Returns:
        - List of all User objects in JSON format
    """
    all_users = [user.to_json() for user in User.all()]
    return jsonify(all_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def view_one_user(user_id: str = None) -> str:
    """GET /api/v1/users/<user_id>
    Returns:
        - User object in JSON format
        - 404 error if User ID doesn't exist
    """
    if user_id is None:
        abort(404)

    if user_id == 'me':
        if request.current_user is None:
            abort(404)
        return jsonify(request.current_user.to_json())

    user = User.get(user_id)
    if user is None:
        abort(404)

    return jsonify(user.to_json())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id: str = None) -> str:
    """DELETE /api/v1/users/<user_id>
    Returns:
        - Empty JSON if User was successfully deleted
        - 404 error if User ID doesn't exist
    """
    if user_id is None:
        abort(404)

    user = User.get(user_id)
    if user is None:
        abort(404)

    user.remove()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user() -> str:
    """POST /api/v1/users
    JSON Body:
        - email (required)
        - password (required)
        - first_name (optional)
        - last_name (optional)
    Returns:
        - User object in JSON format if successful
        - 400 error if creation fails
    """
    rj = None
    try:
        rj = request.get_json()
    except Exception:
        return jsonify({'error': 'Wrong format'}), 400

    email = rj.get("email")
    password = rj.get("password")

    if not email:
        return jsonify({'error': 'email missing'}), 400
    if not password:
        return jsonify({'error': 'password missing'}), 400

    try:
        user = User()
        user.email = email
        user.password = password
        user.first_name = rj.get("first_name")
        user.last_name = rj.get("last_name")
        user.save()
        return jsonify(user.to_json()), 201
    except Exception as e:
        return jsonify({'error': f"Can't create User: {e}"}), 400


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id: str = None) -> str:
    """PUT /api/v1/users/<user_id>
    JSON Body:
        - first_name (optional)
        - last_name (optional)
    Returns:
        - User object in JSON format if successful
        - 404 error if User ID doesn't exist
        - 400 error if update fails
    """
    if user_id is None:
        abort(404)

    user = User.get(user_id)
    if user is None:
        abort(404)

    try:
        rj = request.get_json()
    except Exception:
        return jsonify({'error': 'Wrong format'}), 400

    if rj.get('first_name'):
        user.first_name = rj.get('first_name')
    if rj.get('last_name'):
        user.last_name = rj.get('last_name')

    try:
        user.save()
        return jsonify(user.to_json()), 200
    except Exception as e:
        return jsonify({'error': f"Can't update User: {e}"}), 400

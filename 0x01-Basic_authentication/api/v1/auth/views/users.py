#!/usr/bin/env python3
"""Module of Users views."""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def view_all_users() -> str:
    """GET /api/v1/users
    Returns:
        JSON: List of all User objects represented in JSON.
    """
    all_users = [user.to_json() for user in User.all()]
    return jsonify(all_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def view_one_user(user_id: str) -> str:
    """GET /api/v1/users/<user_id>
    Path parameter:
        user_id: ID of the user to retrieve.
    Returns:
        JSON: User object represented in JSON.
        404: If the User ID does not exist.
    """
    user = User.get(user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_json())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id: str) -> str:
    """DELETE /api/v1/users/<user_id>
    Path parameter:
        user_id: ID of the user to delete.
    Returns:
        JSON: Empty JSON if the user has been deleted.
        404: If the User ID does not exist.
    """
    user = User.get(user_id)
    if user is None:
        abort(404)
    user.remove()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user() -> str:
    """POST /api/v1/users/
    JSON body:
        email: User's email.
        password: User's password.
        last_name: (Optional) User's last name.
        first_name: (Optional) User's first name.
    Returns:
        JSON: User object represented in JSON if creation is successful.
        400: If there is a problem with the request or creation.
    """
    try:
        rj = request.get_json()
    except Exception:
        return jsonify({'error': "Wrong format"}), 400

    email = rj.get("email")
    password = rj.get("password")

    if not email:
        return jsonify({'error': "email missing"}), 400
    if not password:
        return jsonify({'error': "password missing"}), 400

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
def update_user(user_id: str) -> str:
    """PUT /api/v1/users/<user_id>
    Path parameter:
        user_id: ID of the user to update.
    JSON body:
        last_name: (Optional) New last name.
        first_name: (Optional) New first name.
    Returns:
        JSON: Updated User object represented in JSON.
        404: If the User ID does not exist.
        400: If there is a problem with the update request.
    """
    user = User.get(user_id)
    if user is None:
        abort(404)

    try:
        rj = request.get_json()
    except Exception:
        return jsonify({'error': "Wrong format"}), 400

    if rj.get('first_name') is not None:
        user.first_name = rj.get('first_name')
    if rj.get('last_name') is not None:
        user.last_name = rj.get('last_name')

    user.save()
    return jsonify(user.to_json()), 200


#!/usr/bin/env python3
"""Module of Users views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User


def get_user_by_id(user_id: str):
    """Helper function to retrieve a user by ID."""
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)
    return user


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def view_all_users() -> str:
    """GET /api/v1/users
    Return:
      - list of all User objects JSON represented
    """
    all_users = [user.to_json() for user in User.all()]
    return jsonify(all_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def view_one_user(user_id: str) -> str:
    """GET /api/v1/users/:id
    Path parameter:
      - User ID
    Return:
      - User object JSON represented
      - 404 if the User ID doesn't exist
    """
    user = get_user_by_id(user_id)
    return jsonify(user.to_json())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id: str) -> str:
    """DELETE /api/v1/users/:id
    Path parameter:
      - User ID
    Return:
      - empty JSON if the User has been correctly deleted
      - 404 if the User ID doesn't exist
    """
    user = get_user_by_id(user_id)
    user.remove()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user() -> str:
    """POST /api/v1/users/
    JSON body:
      - email
      - password
      - last_name (optional)
      - first_name (optional)
    Return:
      - User object JSON represented
      - 400 if can't create the new User
    """
    data = None
    error_msg = None
    try:
        data = request.get_json()
    except Exception:
        data = None

    if data is None:
        error_msg = "Wrong format"
    elif not data.get("email"):
        error_msg = "email missing"
    elif not data.get("password"):
        error_msg = "password missing"

    if error_msg:
        return jsonify({'error': error_msg}), 400

    try:
        user = User()
        user.email = data.get("email")
        user.password = data.get("password")
        user.first_name = data.get("first_name")
        user.last_name = data.get("last_name")
        user.save()
        return jsonify(user.to_json()), 201
    except Exception as e:
        return jsonify({'error': f"Can't create User: {e}"}), 400


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id: str) -> str:
    """PUT /api/v1/users/:id
    Path parameter:
      - User ID
    JSON body:
      - last_name (optional)
      - first_name (optional)
    Return:
      - User object JSON represented
      - 404 if the User ID doesn't exist
      - 400 if can't update the User
    """
    user = get_user_by_id(user_id)

    data = None
    try:
        data = request.get_json()
    except Exception:
        return jsonify({'error': "Wrong format"}), 400

    if data.get('first_name') is not None:
        user.first_name = data.get('first_name')
    if data.get('last_name') is not None:
        user.last_name = data.get('last_name')

    try:
        user.save()
        return jsonify(user.to_json()), 200
    except Exception as e:
        return jsonify({'error': f"Can't update User: {e}"}), 400

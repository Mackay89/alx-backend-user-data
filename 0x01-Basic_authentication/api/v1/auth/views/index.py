#!/usr/bin/env python3
"""Module of Index views."""
from flask import jsonify, abort
from api.v1.views import app_views
from models.user import User  # Moved import to the top


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """GET /api/v1/status
    Returns:
        JSON: A JSON response indicating the status of the API.
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats/', methods=['GET'], strict_slashes=False)
def stats() -> str:
    """GET /api/v1/stats
    Returns:
        JSON: A JSON response with the count of User objects.
    """
    stats = {}
    stats['users'] = User.count()
    return jsonify(stats)


@app_views.route('/unauthorized/', methods=['GET'], strict_slashes=False)
def unauthorized_endpoint() -> None:
    """GET /api/v1/unauthorized
    Raises:
        401 Unauthorized: Indicates that the request requires user authentication.
    """
    abort(401)


@app_views.route('/forbidden/', methods=['GET'], strict_slashes=False)
def forbidden_endpoint() -> None:
    """GET /api/v1/forbidden
    Raises:
        403 Forbidden: Indicates that the server understands the request but refuses to authorize it.
    """
    abort(403)


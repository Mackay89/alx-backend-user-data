#!/usr/bin/env python3
"""Module of Index views
"""
from flask import jsonify, abort
from api.v1.views import app_views
from models.user import User


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """GET /api/v1/status
    Return:
      - The status of the API
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats() -> str:
    """GET /api/v1/stats
    Return:
      - The number of each object
    """
    stats = {'users': User.count()}
    return jsonify(stats)


@app_views.route('/unauthorized', methods=['GET'], strict_slashes=False)
def unauthorized_endpoint() -> None:
    """GET /api/v1/unauthorized
    Return:
      - Raises a 401 Unauthorized error
    """
    abort(401)


@app_views.route('/forbidden', methods=['GET'], strict_slashes=False)
def forbidden_endpoint() -> None:
    """GET /api/v1/forbidden
    Return:
      - Raises a 403 Forbidden error
    """
    abort(403)

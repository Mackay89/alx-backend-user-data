#!/usr/bin/env python3
"""Module of Index views
"""
from flask import jsonify, abort
from api.v1.views import app_views

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """GET /api/v1/status
    Return:
      - the status of the API
    """
    return jsonify({"status": "OK"})

@app_views.route('/stats/', methods=['GET'], strict_slashes=False)
def stats() -> str:
    """GET /api/v1/stats
    Return:
      - the number of each object type in the database
    """
    from models.user import User
    stats = {'users': User.count()}
    return jsonify(stats)

@app_views.route('/unauthorized/', methods=['GET'], strict_slashes=False)
def unauthorized_endpoint() -> None:
    """GET /api/v1/unauthorized/
    This endpoint raises a 401 Unauthorized error.
    """
    abort(401)

@app_views.route('/forbidden/', methods=['GET'], strict_slashes=False)
def forbidden_endpoint() -> None:
    """GET /api/v1/forbidden/
    This endpoint raises a 403 Forbidden error.
    """
    abort(403)


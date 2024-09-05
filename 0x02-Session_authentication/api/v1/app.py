#!/usr/bin/env python3
"""
Route module for the API
"""


import os
from os import getenv
from typing import Tuple

from flask import Flask, abort, jsonify, request
from flask_cors import CORS, cross_origin

from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth
from api.v1.auth.session_db_auth import SessionDBAuth
from api.v1.auth.session_exp_auth import SessionExpAuth
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
# Create a variable auth initialized to None after the CORS definition
auth = None


# Update api/v1/app.py for using SessionAuth instance for the variable
# auth depending of the value of the environment variable AUTH_TYPE, If
# AUTH_TYPE is equal to session_auth:
#   import SessionAuth from api.v1.auth.session_auth
#   create an instance of SessionAuth and assign it to the variable auth
auth_type = getenv('AUTH_TYPE', 'default')
if auth_type == "session_auth":
    auth = SessionAuth()
elif auth_type == 'session_exp_auth':
    auth = SessionExpAuth()
elif auth_type == 'session_db_auth':
    auth = SessionDBAuth()
elif auth_type == "basic_auth":
    auth = BasicAuth()
else:
    auth = Auth()


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404

"""Contains the token_required decorator to restrict access to authenticated users only and
the admin_required decorator to restrict access to administrators only.
"""
from functools import wraps

from flask import request, jsonify, make_response
import jwt

import config


def user_required(f):
    """Checks for authenticated users with valid token in the header"""

    @wraps(f)
    def decorated(*args, **kwargs):
        """validate token provided"""
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        try:
            data = jwt.decode(token, config.Config.SECRET_KEY) # pylint: disable=W0612
        except:
            return make_response(jsonify({
                "message" : "kindly provide a valid token in the header"}), 401)

        return f(*args, **kwargs)

    return decorated


def admin_required(f):
    """Checks for authenticated admins with valid token in the header"""

    @wraps(f)
    def decorated(*args, **kwargs):
        """validate token provided and ensures the user is an admin"""
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        try:
            data = jwt.decode(token, config.Config.SECRET_KEY)
            if data['usertype'] != "admin":
                return make_response(jsonify({
                    "message" : "Not authorized to perform this function as a non-admin"}), 401)

        except:
            return make_response(jsonify({
                "message" : "kindly provide a valid token in the header"}), 401)

        return f(*args, **kwargs)

    return decorated

def driver_required(f):
    """Checks for authenticated drivers with valid token in the header"""

    @wraps(f)
    def decorated(*args, **kwargs):
        """validate token provided and ensures the user is a driver"""
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        try:
            data = jwt.decode(token, config.Config.SECRET_KEY)
            if data['usertype'] != "driver":
                return make_response(jsonify({
                    "message" : "Not authorized to perform this function as a non-driver"}), 401)
        except:
            return make_response(jsonify({
                "message" : "kindly provide a valid token in the header"}), 401)

        return f(*args, **kwargs)

    return decorated

def driver_admin_required(f):
    """Checks for authenticated driver or admin with valid token in the header"""

    @wraps(f)
    def decorated(*args, **kwargs):
        """validate token provided and ensures the user is a driver or admin"""
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        try:
            data = jwt.decode(token, config.Config.SECRET_KEY)
            if data['usertype'] != "driver" and data['usertype'] != "admin":
                return make_response(jsonify({
                    "message" : "Not authorized to perform this function as a non-driver"}), 401)
        except:
            return make_response(jsonify({
                "message" : "kindly provide a valid token in the header"}), 401)

        return f(*args, **kwargs)

    return decorated

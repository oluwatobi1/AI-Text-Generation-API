from flask import jsonify
from functools import wraps

def response(data, code=0, msg="success", status=200):
    '''
    Application standard response.
    Returns a JSON response with the data, code and status provided.
    '''
    return jsonify({
        "data": data,
        "msg": msg,
        "code": code,
    }), status


def error_response(msg, code=1, status=400):
    """
    Application standard error response.
    """
    return jsonify({
        "msg": msg,
        "code": code,
        "data": None,
    }), status



def custom_response(schema, code=0, msg="success", status=200, many=False):
    """Custom response decorator for Flask-Smorest routes."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            raw_data = func(*args, **kwargs)  
            return response(data=schema(many=many).dump(raw_data), code=code, msg=msg, status=status)
        return wrapper

    return decorator
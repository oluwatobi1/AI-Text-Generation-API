from flask import jsonify

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
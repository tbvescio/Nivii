from functools import wraps
from flask import jsonify
from utils.exception import APIException

def error_handling(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except APIException as e:
            return jsonify({"error": e.message}), e.code
        except Exception as e:
            return jsonify({"error": "An unexpected error occurred.", "details": str(e)}), 500
    return wrapper 
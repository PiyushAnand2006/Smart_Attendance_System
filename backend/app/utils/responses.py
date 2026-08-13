"""API Response Utilities"""
from flask import jsonify

def success_response(data=None, message='Success', meta=None, status_code=200):
    """Return a standardized success response"""
    response = {
        'status': 'success',
        'message': message
    }
    if data is not None:
        response['data'] = data
    if meta:
        response['meta'] = meta
    return jsonify(response), status_code

def error_response(message='An error occurred', code='ERROR', errors=None, status_code=400):
    """Return a standardized error response"""
    response = {
        'status': 'error',
        'message': message,
        'code': code
    }
    if errors:
        response['errors'] = errors
    return jsonify(response), status_code

def paginated_response(items, page, per_page, total, message='Success'):
    """Return a paginated response"""
    return success_response(
        data=items,
        message=message,
        meta={
            'page': page,
            'per_page': per_page,
            'total': total,
            'pages': (total + per_page - 1) // per_page,
            'has_next': page * per_page < total,
            'has_prev': page > 1
        }
    )
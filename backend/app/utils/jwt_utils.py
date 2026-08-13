"""JWT Token Utilities (built on PyJWT, which is installed)."""
from functools import wraps
from datetime import datetime, timedelta, timezone

import jwt
from flask import request, jsonify, current_app


def create_access_token(identity, role, additional_claims=None):
    """Create a signed JWT access token."""
    payload = {
        'sub': identity,
        'role': role,
        'iat': datetime.now(timezone.utc),
        'exp': datetime.now(timezone.utc) + timedelta(hours=24),
        'type': 'access',
    }
    if additional_claims:
        payload.update(additional_claims)
    return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')


def create_refresh_token(identity):
    """Create a long-lived JWT refresh token."""
    payload = {
        'sub': identity,
        'iat': datetime.now(timezone.utc),
        'exp': datetime.now(timezone.utc) + timedelta(days=30),
        'type': 'refresh',
    }
    return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')


def decode_token(token):
    """Decode and validate a JWT. Returns dict with 'error' key on failure."""
    try:
        return jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return {'error': 'TOKEN_EXPIRED', 'message': 'Token has expired'}
    except jwt.InvalidTokenError:
        return {'error': 'TOKEN_INVALID', 'message': 'Invalid token'}


def _extract_token():
    header = request.headers.get('Authorization', '')
    return header.replace('Bearer ', '').strip()


def get_token_identity():
    """Return (identity, role) from the request's bearer token, or (None, None)."""
    token = _extract_token()
    if not token:
        return None, None
    payload = decode_token(token)
    if 'error' in payload:
        return None, None
    return payload.get('sub'), payload.get('role')


def auth_required(f):
    """Decorator: require a valid bearer token."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = _extract_token()
        if not token:
            return jsonify({'status': 'error', 'message': 'Authorization token is required', 'code': 'TOKEN_MISSING'}), 401
        payload = decode_token(token)
        if 'error' in payload:
            return jsonify({'status': 'error', 'message': payload['message'], 'code': payload['error']}), 401
        kwargs['current_user_id'] = payload.get('sub')
        kwargs['current_role'] = payload.get('role')
        return f(*args, **kwargs)
    return wrapper


def role_required(*roles):
    """Decorator: require a valid token AND one of the given roles."""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = _extract_token()
            if not token:
                return jsonify({'status': 'error', 'message': 'Authorization token is required', 'code': 'TOKEN_MISSING'}), 401
            payload = decode_token(token)
            if 'error' in payload:
                return jsonify({'status': 'error', 'message': payload['message'], 'code': payload['error']}), 401
            if payload.get('role') not in roles:
                return jsonify({'status': 'error', 'message': 'Access denied', 'code': 'FORBIDDEN'}), 403
            kwargs['current_user_id'] = payload.get('sub')
            kwargs['current_role'] = payload.get('role')
            return f(*args, **kwargs)
        return wrapper
    return decorator

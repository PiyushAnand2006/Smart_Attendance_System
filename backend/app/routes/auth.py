"""Authentication Routes"""
from flask import Blueprint, request
from app.store import db, hash_pwd
from app.utils.jwt_utils import create_access_token, create_refresh_token, auth_required
import uuid

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json(silent=True) or {}
    email = (data.get('email') or '').strip().lower()
    password = data.get('password') or ''

    user = next((u for u in db['users'] if u['email'] == email), None)
    if not user or user['password'] != hash_pwd(password):
        return {'status': 'error', 'message': 'Invalid email or password'}, 401
    if not user.get('is_active', True):
        return {'status': 'error', 'message': 'Account is disabled'}, 403

    token = create_access_token(user['user_id'], user['role'])
    return {
        'status': 'success',
        'data': {
            'access_token': token,
            'refresh_token': create_refresh_token(user['user_id']),
            'user': {k: v for k, v in user.items() if k != 'password'},
            'role': user['role'],
        }
    }


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json(silent=True) or {}
    email = (data.get('email') or '').strip().lower()
    password = data.get('password') or ''
    first_name = (data.get('first_name') or '').strip()
    last_name = (data.get('last_name') or '').strip()
    role = data.get('role') or 'student'

    if role not in ('student', 'faculty'):
        return {'status': 'error', 'message': 'Invalid role'}, 400
    if not email or not password:
        return {'status': 'error', 'message': 'Email and password are required'}, 400
    if len(password) < 6:
        return {'status': 'error', 'message': 'Password must be at least 6 characters'}, 400
    if any(u['email'] == email for u in db['users']):
        return {'status': 'error', 'message': 'Email already registered'}, 400

    user = {
        'id': len(db['users']) + 1,
        'user_id': f'USR{uuid.uuid4().hex[:8].upper()}',
        'email': email,
        'password': hash_pwd(password),
        'first_name': first_name,
        'last_name': last_name,
        'role': role,
        'is_active': True,
    }
    db['users'].append(user)

    token = create_access_token(user['user_id'], user['role'])
    return {
        'status': 'success',
        'message': 'Account created',
        'data': {
            'access_token': token,
            'user': {k: v for k, v in user.items() if k != 'password'},
            'role': user['role'],
        }
    }, 201


@auth_bp.route('/me', methods=['GET'])
@auth_required
def me(current_user_id, current_role):
    user = next((u for u in db['users'] if u['user_id'] == current_user_id), None)
    if not user:
        return {'status': 'error', 'message': 'User not found'}, 404
    return {'status': 'success', 'data': {k: v for k, v in user.items() if k != 'password'}}

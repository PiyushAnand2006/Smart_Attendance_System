"""Class Routes"""
from flask import Blueprint, request
from app.store import db
from app.utils.jwt_utils import auth_required, role_required

classes_bp = Blueprint('classes', __name__)


@classes_bp.route('/', methods=['GET'])
@auth_required
def get_classes(current_user_id, current_role):
    classes = [c for c in db['classes'] if c.get('is_active', True)]
    return {'status': 'success', 'data': classes}


@classes_bp.route('/', methods=['POST'])
@role_required('admin')
def create_class(current_user_id, current_role):
    data = request.get_json(silent=True) or {}
    name = (data.get('name') or '').strip()
    code = (data.get('code') or '').strip()
    if not name or not code:
        return {'status': 'error', 'message': 'name and code are required'}, 400
    cls = {
        'id': len(db['classes']) + 1,
        'name': name,
        'code': code,
        'department': data.get('department', 'Engineering'),
        'batch_year': data.get('batch_year'),
        'is_active': True,
    }
    db['classes'].append(cls)
    return {'status': 'success', 'message': 'Class created', 'data': cls}, 201


@classes_bp.route('/<int:cid>', methods=['GET'])
@auth_required
def get_class(cid, current_user_id, current_role):
    cls = next((c for c in db['classes'] if c['id'] == cid), None)
    if not cls:
        return {'status': 'error', 'message': 'Class not found'}, 404
    return {'status': 'success', 'data': cls}

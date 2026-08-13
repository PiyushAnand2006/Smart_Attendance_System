"""Subject Routes"""
from flask import Blueprint, request
from app.store import db
from app.utils.jwt_utils import auth_required, role_required

subjects_bp = Blueprint('subjects', __name__)


@subjects_bp.route('/', methods=['GET'])
@auth_required
def get_subjects(current_user_id, current_role):
    department = request.args.get('department')
    subjects = [s for s in db['subjects'] if s.get('is_active', True)]
    if department:
        subjects = [s for s in subjects if s.get('department') == department]
    return {'status': 'success', 'data': subjects, 'meta': {'total': len(subjects)}}


@subjects_bp.route('/', methods=['POST'])
@role_required('admin')
def create_subject(current_user_id, current_role):
    data = request.get_json(silent=True) or {}
    name = (data.get('name') or '').strip()
    code = (data.get('code') or '').strip()
    if not name or not code:
        return {'status': 'error', 'message': 'name and code are required'}, 400
    subject = {
        'id': len(db['subjects']) + 1,
        'name': name,
        'code': code,
        'department': data.get('department', 'CSE'),
        'semester': data.get('semester', 1),
        'credits': data.get('credits', 0),
        'is_active': True,
    }
    db['subjects'].append(subject)
    return {'status': 'success', 'message': 'Subject created', 'data': subject}, 201


@subjects_bp.route('/<int:sid>', methods=['PUT'])
@role_required('admin')
def update_subject(sid, current_user_id, current_role):
    subject = next((s for s in db['subjects'] if s['id'] == sid), None)
    if not subject:
        return {'status': 'error', 'message': 'Subject not found'}, 404
    data = request.get_json(silent=True) or {}
    for key in ('name', 'code', 'department', 'semester', 'credits', 'is_active'):
        if key in data:
            subject[key] = data[key]
    return {'status': 'success', 'message': 'Subject updated', 'data': subject}

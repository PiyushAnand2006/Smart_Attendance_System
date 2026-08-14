"""Subject Routes"""
from flask import Blueprint, request
from app.db import session_scope
from app.models.subject import Subject
from app.utils.jwt_utils import auth_required, role_required

subjects_bp = Blueprint('subjects', __name__)


@subjects_bp.route('/', methods=['GET'])
@auth_required
def get_subjects(current_user_id, current_role):
    department = request.args.get('department')
    with session_scope() as s:
        q = s.query(Subject).filter_by(is_active=True)
        if department:
            q = q.filter_by(department=department)
        return {'status': 'success', 'data': [sub.to_dict() for sub in q.all()], 'meta': {'total': q.count()}}


@subjects_bp.route('/', methods=['POST'])
@role_required('admin')
def create_subject(current_user_id, current_role):
    data = request.get_json(silent=True) or {}
    name = (data.get('name') or '').strip()
    code = (data.get('code') or '').strip()
    if not name or not code:
        return {'status': 'error', 'message': 'name and code are required'}, 400
    with session_scope() as s:
        subject = Subject(
            name=name, code=code, department=data.get('department', 'CSE'),
            semester=data.get('semester', 1), credits=data.get('credits', 0), is_active=True,
        )
        s.add(subject)
        s.flush()
        return {'status': 'success', 'message': 'Subject created', 'data': subject.to_dict()}, 201


@subjects_bp.route('/<int:sid>', methods=['PUT'])
@role_required('admin')
def update_subject(sid, current_user_id, current_role):
    data = request.get_json(silent=True) or {}
    with session_scope() as s:
        subject = s.query(Subject).filter_by(id=sid).first()
        if not subject:
            return {'status': 'error', 'message': 'Subject not found'}, 404
        for key in ('name', 'code', 'department', 'semester', 'credits', 'is_active'):
            if key in data:
                setattr(subject, key, data[key])
        s.flush()
        return {'status': 'success', 'message': 'Subject updated', 'data': subject.to_dict()}

"""Class Routes"""
from flask import Blueprint, request
from app.db import session_scope
from app.models.class_ import ClassModel
from app.utils.jwt_utils import auth_required, role_required

classes_bp = Blueprint('classes', __name__)


@classes_bp.route('/', methods=['GET'])
@auth_required
def get_classes(current_user_id, current_role):
    with session_scope() as s:
        classes = s.query(ClassModel).filter_by(is_active=True).all()
        return {'status': 'success', 'data': [c.to_dict() for c in classes]}


@classes_bp.route('/', methods=['POST'])
@role_required('admin')
def create_class(current_user_id, current_role):
    data = request.get_json(silent=True) or {}
    name = (data.get('name') or '').strip()
    code = (data.get('code') or '').strip()
    if not name or not code:
        return {'status': 'error', 'message': 'name and code are required'}, 400
    with session_scope() as s:
        cls = ClassModel(name=name, code=code, department=data.get('department', 'Engineering'),
                         batch_year=data.get('batch_year'), is_active=True)
        s.add(cls)
        s.flush()
        return {'status': 'success', 'message': 'Class created', 'data': cls.to_dict()}, 201


@classes_bp.route('/<int:cid>', methods=['GET'])
@auth_required
def get_class(cid, current_user_id, current_role):
    with session_scope() as s:
        cls = s.query(ClassModel).filter_by(id=cid).first()
        if not cls:
            return {'status': 'error', 'message': 'Class not found'}, 404
        return {'status': 'success', 'data': cls.to_dict()}

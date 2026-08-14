"""Notifications Routes"""
from flask import Blueprint, request
from app.db import session_scope
from app.models.notification import NotificationQueue, NotificationTemplate
from app.models.student import ParentGuardian, Student
from app.utils.jwt_utils import auth_required, role_required

notifications_bp = Blueprint('notifications', __name__)


@notifications_bp.route('/templates', methods=['GET'])
@auth_required
def get_templates(current_user_id, current_role):
    with session_scope() as s:
        return {'status': 'success', 'data': [t.to_dict() for t in s.query(NotificationTemplate).all()]}


@notifications_bp.route('/templates', methods=['POST'])
@role_required('admin')
def create_template(current_user_id, current_role):
    data = request.get_json(silent=True) or {}
    name = (data.get('name') or '').strip()
    content = (data.get('content') or '').strip()
    if not name or not content:
        return {'status': 'error', 'message': 'name and content are required'}, 400
    with session_scope() as s:
        template = NotificationTemplate(
            name=name, display_name=data.get('display_name') or name,
            content=content, is_active=data.get('is_active', True),
        )
        s.add(template)
        s.flush()
        return {'status': 'success', 'message': 'Template created', 'data': template.to_dict()}, 201


@notifications_bp.route('/queue', methods=['GET'])
@role_required('admin')
def get_queue(current_user_id, current_role):
    with session_scope() as s:
        queue = s.query(NotificationQueue).order_by(NotificationQueue.id.desc()).limit(50).all()
        return {'status': 'success', 'data': [q.to_dict() for q in queue]}


@notifications_bp.route('/mine', methods=['GET'])
@role_required('student')
def get_mine(current_user_id, current_role):
    with session_scope() as s:
        student = s.query(Student).filter_by(student_id=current_user_id).first()
        if not student:
            return {'status': 'success', 'data': []}
        parent = s.query(ParentGuardian).filter_by(student_id=student.id).first()
        if not parent:
            return {'status': 'success', 'data': []}
        queue = (s.query(NotificationQueue)
                 .filter_by(recipient_number=parent.whatsapp_number, status='SENT')
                 .order_by(NotificationQueue.id.desc())
                 .all())
        return {'status': 'success', 'data': [q.to_dict() for q in queue]}


@notifications_bp.route('/process', methods=['POST'])
@role_required('admin')
def process_queue(current_user_id, current_role):
    with session_scope() as s:
        for n in s.query(NotificationQueue).filter_by(status='PENDING').all():
            n.status = 'SENT'
        s.flush()
        return {'status': 'success', 'message': 'Notifications processed'}

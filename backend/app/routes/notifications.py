"""Notifications Routes"""
from flask import Blueprint, request
from app.store import db
from app.utils.jwt_utils import auth_required, role_required

notifications_bp = Blueprint('notifications', __name__)


@notifications_bp.route('/templates', methods=['GET'])
@auth_required
def get_templates(current_user_id, current_role):
    return {'status': 'success', 'data': db['notification_templates']}


@notifications_bp.route('/templates', methods=['POST'])
@role_required('admin')
def create_template(current_user_id, current_role):
    data = request.get_json(silent=True) or {}
    name = (data.get('name') or '').strip()
    content = (data.get('content') or '').strip()
    if not name or not content:
        return {'status': 'error', 'message': 'name and content are required'}, 400
    template = {
        'id': len(db['notification_templates']) + 1,
        'name': name,
        'display_name': data.get('display_name') or name,
        'content': content,
        'is_active': data.get('is_active', True),
    }
    db['notification_templates'].append(template)
    return {'status': 'success', 'message': 'Template created', 'data': template}, 201


@notifications_bp.route('/queue', methods=['GET'])
@role_required('admin')
def get_queue(current_user_id, current_role):
    queue = sorted(db['notification_queue'], key=lambda n: n.get('created_at', ''), reverse=True)[:50]
    return {'status': 'success', 'data': queue}


@notifications_bp.route('/process', methods=['POST'])
@role_required('admin')
def process_queue(current_user_id, current_role):
    # Mock processing: mark pending notifications as sent
    for n in db['notification_queue']:
        if n['status'] == 'PENDING':
            n['status'] = 'SENT'
    return {'status': 'success', 'message': 'Notifications processed'}

"""QR Code Routes"""
from flask import Blueprint, request
from app.store import db
from app.utils.jwt_utils import role_required
from datetime import datetime, timedelta
import uuid

qr_bp = Blueprint('qr', __name__)

# Ephemeral session QR tokens (kept in memory)
qr_tokens = {}


@qr_bp.route('/generate', methods=['POST'])
@role_required('faculty', 'admin')
def generate(current_user_id, current_role):
    data = request.get_json(silent=True) or {}
    session_id = data.get('session_id')
    if not session_id:
        return {'status': 'error', 'message': 'session_id is required'}, 400

    token = f'TKN{uuid.uuid4().hex[:12].upper()}'
    expires_at = datetime.utcnow() + timedelta(seconds=60)
    qr_tokens[token] = {'session_id': int(session_id), 'expires_at': expires_at}

    return {
        'status': 'success',
        'data': {'token': token, 'expires_at': expires_at.isoformat(), 'expires_in': 60},
    }


@qr_bp.route('/scan', methods=['POST'])
@role_required('student', 'faculty', 'admin')
def scan(current_user_id, current_role):
    data = request.get_json(silent=True) or {}
    token = data.get('token') or data.get('qr_code')
    student_id = data.get('student_id')

    if not token:
        return {'status': 'error', 'message': 'QR token is required'}, 400

    entry = qr_tokens.get(token)
    if not entry:
        return {'status': 'error', 'message': 'Invalid or expired QR code'}, 400
    if entry['expires_at'] < datetime.utcnow():
        qr_tokens.pop(token, None)
        return {'status': 'error', 'message': 'QR code expired'}, 400

    session_id = entry['session_id']
    if not student_id:
        return {'status': 'error', 'message': 'student_id is required'}, 400

    # Students may only mark their own attendance
    if current_role == 'student':
        student = next((s for s in db['students'] if s['student_id'] == current_user_id), None)
        if not student or student['id'] != int(student_id):
            return {'status': 'error', 'message': 'You can only mark your own attendance'}, 403

    if any(r['student_id'] == int(student_id) and r['session_id'] == session_id for r in db['attendance_records']):
        return {'status': 'error', 'message': 'Attendance already marked'}, 400

    record = {
        'id': len(db['attendance_records']) + 1,
        'student_id': int(student_id),
        'session_id': session_id,
        'status': 'PRESENT',
        'attendance_method': 'QR',
        'attendance_date': datetime.utcnow().date().isoformat(),
        'created_at': datetime.utcnow().isoformat(),
    }
    db['attendance_records'].append(record)
    return {'status': 'success', 'message': 'Attendance marked via QR', 'data': record}, 201


@qr_bp.route('/scan-my', methods=['POST'])
@role_required('student')
def scan_my(current_user_id, current_role):
    data = request.get_json(silent=True) or {}
    token = data.get('token') or data.get('qr_code')
    if not token:
        return {'status': 'error', 'message': 'QR token is required'}, 400
    entry = qr_tokens.get(token)
    if not entry:
        return {'status': 'error', 'message': 'Invalid or expired QR code'}, 400
    if entry['expires_at'] < datetime.utcnow():
        qr_tokens.pop(token, None)
        return {'status': 'error', 'message': 'QR code expired'}, 400
    session_id = entry['session_id']
    student = next((s for s in db['students'] if s['student_id'] == current_user_id), None)
    if not student:
        return {'status': 'error', 'message': 'Student profile not found'}, 404
    if any(r['student_id'] == student['id'] and r['session_id'] == session_id for r in db['attendance_records']):
        return {'status': 'error', 'message': 'Attendance already marked'}, 400
    record = {
        'id': len(db['attendance_records']) + 1,
        'student_id': student['id'],
        'session_id': session_id,
        'status': 'PRESENT',
        'attendance_method': 'QR',
        'attendance_date': datetime.utcnow().date().isoformat(),
        'created_at': datetime.utcnow().isoformat(),
    }
    db['attendance_records'].append(record)
    session = next((s for s in db['attendance_sessions'] if s['id'] == session_id), None)
    subject = next((s for s in db['subjects'] if s['id'] == (session['subject_id'] if session else 0)), None)
    return {'status': 'success', 'message': 'Attendance marked!', 'data': {**record, 'subject_name': subject['name'] if subject else None}}, 201
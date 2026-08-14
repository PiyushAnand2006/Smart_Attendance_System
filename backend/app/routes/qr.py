"""QR Code Routes"""
from flask import Blueprint, current_app, request
from app.db import session_scope
from app.models.attendance import AttendanceRecord, AttendanceSession
from app.models.qr import QRToken
from app.models.student import Student
from app.models.subject import Subject
from app.utils.jwt_utils import role_required
from datetime import datetime, timedelta
import uuid

qr_bp = Blueprint('qr', __name__)


def _expiry_seconds():
    try:
        return int(current_app.config.get('QR_TOKEN_EXPIRY_SECONDS', 60))
    except (TypeError, ValueError):
        return 60


@qr_bp.route('/generate', methods=['POST'])
@role_required('faculty', 'admin')
def generate(current_user_id, current_role):
    data = request.get_json(silent=True) or {}
    session_id = data.get('session_id')
    if not session_id:
        return {'status': 'error', 'message': 'session_id is required'}, 400
    with session_scope() as s:
        sess = s.query(AttendanceSession).filter_by(id=int(session_id)).first()
        if not sess:
            return {'status': 'error', 'message': 'Session not found'}, 404
        token = f'TKN{uuid.uuid4().hex[:12].upper()}'
        expires_at = datetime.utcnow() + timedelta(seconds=_expiry_seconds())
        s.add(QRToken(token=token, session_id=int(session_id), expires_at=expires_at.isoformat(), is_active=True))
        s.flush()
        return {'status': 'success', 'data': {'token': token, 'expires_at': expires_at.isoformat(), 'expires_in': _expiry_seconds()}}


@qr_bp.route('/scan', methods=['POST'])
@role_required('student', 'faculty', 'admin')
def scan(current_user_id, current_role):
    data = request.get_json(silent=True) or {}
    token = data.get('token') or data.get('qr_code')
    student_id = data.get('student_id')
    if not token:
        return {'status': 'error', 'message': 'QR token is required'}, 400
    with session_scope() as s:
        entry = s.query(QRToken).filter_by(token=token, is_active=True).first()
        if not entry:
            return {'status': 'error', 'message': 'Invalid or expired QR code'}, 400
        if datetime.fromisoformat(entry.expires_at) < datetime.utcnow():
            entry.is_active = False
            s.flush()
            return {'status': 'error', 'message': 'QR code expired'}, 400
        session_id = entry.session_id
        if not student_id:
            return {'status': 'error', 'message': 'student_id is required'}, 400
        student_id = int(student_id)

        if current_role == 'student':
            student = s.query(Student).filter_by(student_id=current_user_id).first()
            if not student or student.id != student_id:
                return {'status': 'error', 'message': 'You can only mark your own attendance'}, 403

        if s.query(AttendanceRecord).filter_by(student_id=student_id, session_id=session_id).first():
            return {'status': 'error', 'message': 'Attendance already marked'}, 400

        record = AttendanceRecord(student_id=student_id, session_id=session_id, status='PRESENT',
                                  attendance_method='QR', attendance_date=datetime.utcnow().date(),
                                  created_at=datetime.utcnow())
        s.add(record)
        s.flush()
        return {'status': 'success', 'message': 'Attendance marked via QR', 'data': record.to_dict()}, 201


@qr_bp.route('/scan-my', methods=['POST'])
@role_required('student')
def scan_my(current_user_id, current_role):
    data = request.get_json(silent=True) or {}
    token = data.get('token') or data.get('qr_code')
    if not token:
        return {'status': 'error', 'message': 'QR token is required'}, 400
    with session_scope() as s:
        entry = s.query(QRToken).filter_by(token=token, is_active=True).first()
        if not entry:
            return {'status': 'error', 'message': 'Invalid or expired QR code'}, 400
        if datetime.fromisoformat(entry.expires_at) < datetime.utcnow():
            entry.is_active = False
            s.flush()
            return {'status': 'error', 'message': 'QR code expired'}, 400
        session_id = entry.session_id
        student = s.query(Student).filter_by(student_id=current_user_id).first()
        if not student:
            return {'status': 'error', 'message': 'Student profile not found'}, 404
        if s.query(AttendanceRecord).filter_by(student_id=student.id, session_id=session_id).first():
            return {'status': 'error', 'message': 'Attendance already marked'}, 400
        record = AttendanceRecord(student_id=student.id, session_id=session_id, status='PRESENT',
                                  attendance_method='QR', attendance_date=datetime.utcnow().date(),
                                  created_at=datetime.utcnow())
        s.add(record)
        s.flush()
        sess = s.query(AttendanceSession).filter_by(id=session_id).first()
        subject = s.query(Subject).filter_by(id=sess.subject_id).first() if sess else None
        return {'status': 'success', 'message': 'Attendance marked!',
                'data': {**record.to_dict(), 'subject_name': subject.name if subject else None}}, 201

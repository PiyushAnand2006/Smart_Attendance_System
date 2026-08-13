"""Attendance Routes"""
from flask import Blueprint, request
from app.store import db
from app.utils.jwt_utils import role_required
from datetime import date, datetime
import uuid

attendance_bp = Blueprint('attendance', __name__)


@attendance_bp.route('/sessions', methods=['GET'])
@role_required('faculty', 'admin')
def get_sessions(current_user_id, current_role):
    sessions = []
    for s in db['attendance_sessions']:
        subject = next((x for x in db['subjects'] if x['id'] == s['subject_id']), None)
        cls = next((x for x in db['classes'] if x['id'] == s['class_id']), None)
        sessions.append({
            **s,
            'subject_name': subject['name'] if subject else None,
            'class_name': cls['name'] if cls else None,
            'marked': sum(1 for r in db['attendance_records'] if r['session_id'] == s['id']),
        })
    return {'status': 'success', 'data': sessions}


@attendance_bp.route('/sessions', methods=['POST'])
@role_required('faculty', 'admin')
def create_session(current_user_id, current_role):
    data = request.get_json(silent=True) or {}
    subject_id = data.get('subject_id') or data.get('subject')
    class_id = data.get('class_id') or data.get('class')
    if not subject_id or not class_id:
        return {'status': 'error', 'message': 'subject_id and class_id are required'}, 400

    session = {
        'id': len(db['attendance_sessions']) + 1,
        'session_id': f'SES{uuid.uuid4().hex[:8].upper()}',
        'subject_id': int(subject_id),
        'class_id': int(class_id),
        'faculty_id': data.get('faculty_id', 1),
        'attendance_mode': (data.get('mode') or data.get('attendance_mode') or 'FACE').upper(),
        'status': 'active',
        'total_students': len([s for s in db['students'] if s.get('class_id') == int(class_id)]),
        'scheduled_date': data.get('scheduled_date') or date.today().isoformat(),
        'created_at': datetime.utcnow().isoformat(),
    }
    db['attendance_sessions'].append(session)
    return {'status': 'success', 'message': 'Session created', 'data': session}, 201


@attendance_bp.route('/sessions/<int:sid>', methods=['GET'])
@role_required('faculty', 'admin', 'student')
def get_session(sid, current_user_id, current_role):
    s = next((x for x in db['attendance_sessions'] if x['id'] == sid), None)
    if not s:
        return {'status': 'error', 'message': 'Session not found'}, 404
    records = [r for r in db['attendance_records'] if r['session_id'] == sid]
    subject = next((x for x in db['subjects'] if x['id'] == s['subject_id']), None)
    return {
        'status': 'success',
        'data': {
            **s,
            'subject_name': subject['name'] if subject else None,
            'records': records,
            'present': sum(1 for r in records if r['status'] in ('PRESENT', 'LATE')),
        }
    }


@attendance_bp.route('/sessions/<int:sid>/mark', methods=['POST'])
@role_required('faculty', 'admin')
def mark_attendance(sid, current_user_id, current_role):
    s = next((x for x in db['attendance_sessions'] if x['id'] == sid), None)
    if not s:
        return {'status': 'error', 'message': 'Session not found'}, 404

    data = request.get_json(silent=True) or {}
    student_id = data.get('student_id') or data.get('student')
    if not student_id:
        return {'status': 'error', 'message': 'student_id is required'}, 400

    if any(r['student_id'] == int(student_id) and r['session_id'] == sid for r in db['attendance_records']):
        return {'status': 'error', 'message': 'Attendance already marked for this student'}, 400

    record = {
        'id': len(db['attendance_records']) + 1,
        'student_id': int(student_id),
        'session_id': sid,
        'status': data.get('status', 'PRESENT').upper(),
        'attendance_method': (data.get('method') or data.get('attendance_method') or 'FACE').upper(),
        'attendance_date': date.today().isoformat(),
        'created_at': datetime.utcnow().isoformat(),
    }
    db['attendance_records'].append(record)

    # Queue a WhatsApp notification for the student's parent (mock mode)
    student = next((x for x in db['students'] if x['id'] == int(student_id)), None)
    if student:
        parent = next((p for p in db['parents'] if p['student_id'] == int(student_id)), None)
        if parent:
            db['notification_queue'].append({
                'id': len(db['notification_queue']) + 1,
                'session_id': sid,
                'recipient_number': parent['whatsapp_number'],
                'message': f"Attendance marked for {student['first_name']} {student['last_name']}",
                'status': 'SENT',
                'created_at': datetime.utcnow().isoformat(),
            })

    return {'status': 'success', 'message': 'Attendance marked', 'data': record}, 201


@attendance_bp.route('/sessions/<int:sid>/end', methods=['POST'])
@role_required('faculty', 'admin')
def end_session(sid, current_user_id, current_role):
    s = next((x for x in db['attendance_sessions'] if x['id'] == sid), None)
    if not s:
        return {'status': 'error', 'message': 'Session not found'}, 404
    s['status'] = 'completed'
    return {'status': 'success', 'message': 'Session ended', 'data': s}


@attendance_bp.route('/sessions/<int:sid>/batch-mark', methods=['POST'])
@role_required('faculty', 'admin')
def batch_mark(sid, current_user_id, current_role):
    s = next((x for x in db['attendance_sessions'] if x['id'] == sid), None)
    if not s:
        return {'status': 'error', 'message': 'Session not found'}, 404
    data = request.get_json(silent=True) or {}
    records = data.get('records', [])
    created = []
    for rec in records:
        student_id = rec.get('student_id')
        status = (rec.get('status') or 'PRESENT').upper()
        if any(r['student_id'] == int(student_id) and r['session_id'] == sid for r in db['attendance_records']):
            continue
        record = {
            'id': len(db['attendance_records']) + 1,
            'student_id': int(student_id),
            'session_id': sid,
            'status': status,
            'attendance_method': (rec.get('method') or 'MANUAL').upper(),
            'attendance_date': date.today().isoformat(),
            'created_at': datetime.utcnow().isoformat(),
        }
        db['attendance_records'].append(record)
        created.append(record)
    return {'status': 'success', 'message': f'{len(created)} records created', 'data': created}


@attendance_bp.route('/my-attendance', methods=['GET'])
@role_required('student')
def my_attendance(current_user_id, current_role):
    student = next((s for s in db['students'] if s['student_id'] == current_user_id), None)
    if not student:
        return {'status': 'error', 'message': 'Student not found'}, 404
    records = [r for r in db['attendance_records'] if r['student_id'] == student['id']]
    # Group by session for enrichment
    enriched = []
    for r in records:
        session = next((s for s in db['attendance_sessions'] if s['id'] == r['session_id']), None)
        subject = next((s for s in db['subjects'] if s['id'] == (session['subject_id'] if session else 0)), None)
        enriched.append({**r, 'subject_name': subject['name'] if subject else None, 'subject_code': subject['code'] if subject else None})
    return {'status': 'success', 'data': enriched}
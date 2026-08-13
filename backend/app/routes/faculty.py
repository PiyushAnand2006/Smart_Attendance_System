"""Faculty Routes"""
from flask import Blueprint, request
from app.store import db
from app.utils.jwt_utils import role_required
from datetime import date

faculty_bp = Blueprint('faculty', __name__)


@faculty_bp.route('/dashboard', methods=['GET'])
@role_required('faculty', 'admin')
def get_dashboard(current_user_id, current_role):
    today = date.today().isoformat()
    sessions = [s for s in db['attendance_sessions'] if s.get('scheduled_date') == today]
    records = [r for r in db['attendance_records'] if r.get('attendance_date') == today]
    total = len(records)
    present = sum(1 for r in records if r['status'] in ('PRESENT', 'LATE'))

    session_list = []
    for s in sessions:
        subject = next((x for x in db['subjects'] if x['id'] == s['subject_id']), None)
        cls = next((x for x in db['classes'] if x['id'] == s['class_id']), None)
        session_list.append({
            'id': s['id'],
            'session_id': s['session_id'],
            'subject_name': subject['name'] if subject else 'Unknown',
            'class_name': f"{cls['code']}-{s.get('section', 'A')}" if cls else 'Unknown',
            'time': s.get('scheduled_date'),
            'status': s['status'],
            'mode': s['attendance_mode'],
        })

    return {
        'status': 'success',
        'data': {
            'today_date': today,
            'today_sessions': session_list,
            'today_total': total,
            'today_present': present,
            'today_absent': total - present,
            'attendance_rate': round(present / total * 100, 1) if total > 0 else 0,
        }
    }


@faculty_bp.route('/schedule', methods=['GET'])
@role_required('faculty', 'admin')
def get_schedule(current_user_id, current_role):
    day = request.args.get('day', date.today().weekday(), type=int)
    sessions = [s for s in db['attendance_sessions'] if s.get('scheduled_date') == date.today().isoformat()]
    result = []
    for s in sessions:
        subject = next((x for x in db['subjects'] if x['id'] == s['subject_id']), None)
        result.append({
            'id': s['id'],
            'subject': subject,
            'class_id': s['class_id'],
            'attendance_mode': s['attendance_mode'],
            'status': s['status'],
            'scheduled_date': s.get('scheduled_date'),
        })
    return {'status': 'success', 'data': result}


@faculty_bp.route('/students', methods=['GET'])
@role_required('faculty', 'admin')
def get_faculty_students(current_user_id, current_role):
    students = []
    for s in db['students']:
        if not s.get('is_active', True): continue
        parent = next((p for p in db['parents'] if p['student_id'] == s['id']), None)
        qr = next((q for q in db['qr_identities'] if q['student_id'] == s['id']), None)
        students.append({**s, 'full_name': f"{s['first_name']} {s['last_name']}", 'parent': bool(parent), 'face': s.get('enrollment_status') in ('ready', 'face_enrolled'), 'qr': bool(qr and qr.get('is_active'))})
    return {'status': 'success', 'data': students}


@faculty_bp.route('/students/<int:sid>/enroll-face', methods=['POST'])
@role_required('faculty', 'admin')
def enroll_face(sid, current_user_id, current_role):
    from flask import jsonify
    student = next((s for s in db['students'] if s['id'] == sid), None)
    if not student:
        return {'status': 'error', 'message': 'Student not found'}, 404
    student['enrollment_status'] = 'face_enrolled'
    return {'status': 'success', 'message': 'Face enrolled for ' + student['first_name'], 'data': {'student_id': sid, 'status': 'face_enrolled'}}
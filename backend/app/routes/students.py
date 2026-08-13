"""Student Routes"""
from flask import Blueprint, request
from app.store import db
from app.utils.jwt_utils import auth_required, role_required
import uuid

students_bp = Blueprint('students', __name__)


def _student_summary(s):
    """Enrich a student with face/qr/parent readiness and attendance."""
    parent = next((p for p in db['parents'] if p['student_id'] == s['id']), None)
    qr = next((q for q in db['qr_identities'] if q['student_id'] == s['id']), None)
    records = [r for r in db['attendance_records'] if r['student_id'] == s['id']]
    present = sum(1 for r in records if r['status'] in ('PRESENT', 'LATE'))
    return {
        **s,
        'full_name': f"{s['first_name']} {s['last_name']}",
        'parent': bool(parent),
        'face': s.get('enrollment_status') in ('ready', 'face_enrolled'),
        'qr': bool(qr and qr.get('is_active')),
        'overall_attendance': round(present / len(records) * 100, 1) if records else 0.0,
    }


@students_bp.route('/', methods=['GET'])
@auth_required
def get_students(current_user_id, current_role):
    students = [_student_summary(s) for s in db['students'] if s.get('is_active', True)]
    return {'status': 'success', 'data': students, 'meta': {'total': len(students)}}


@students_bp.route('/<int:sid>', methods=['GET'])
@auth_required
def get_student(sid, current_user_id, current_role):
    s = next((x for x in db['students'] if x['id'] == sid), None)
    if not s:
        return {'status': 'error', 'message': 'Student not found'}, 404
    return {'status': 'success', 'data': _student_summary(s)}


@students_bp.route('/', methods=['POST'])
@role_required('admin', 'faculty')
def create_student(current_user_id, current_role):
    data = request.get_json(silent=True) or {}
    first_name = (data.get('first_name') or '').strip()
    last_name = (data.get('last_name') or '').strip()
    if not first_name or not last_name:
        return {'status': 'error', 'message': 'first_name and last_name are required'}, 400

    student = {
        'id': len(db['students']) + 1,
        'student_id': f'STU{len(db["students"]) + 1:04d}',
        'first_name': first_name,
        'last_name': last_name,
        'roll_number': data.get('roll_number') or f'42{len(db["students"]) + 1:02d}',
        'class_id': data.get('class_id', 1),
        'section': data.get('section', 'A'),
        'department': data.get('department', 'CSE'),
        'enrollment_status': 'incomplete',
        'is_active': True,
    }
    db['students'].append(student)
    db['parents'].append({
        'id': len(db['parents']) + 1,
        'student_id': student['id'],
        'name': data.get('parent_name') or f'Mr. {last_name}',
        'whatsapp_number': data.get('parent_whatsapp') or f'+9198765{len(db["parents"]) + 1:05d}',
        'relationship': 'father',
    })
    db['qr_identities'].append({
        'id': len(db['qr_identities']) + 1,
        'student_id': student['id'],
        'qr_identifier': f'QR{uuid.uuid4().hex[:8].upper()}',
        'is_active': True,
    })
    return {'status': 'success', 'message': 'Student created', 'data': _student_summary(student)}, 201


@students_bp.route('/<int:sid>/attendance', methods=['GET'])
@auth_required
def student_attendance(sid, current_user_id, current_role):
    s = next((x for x in db['students'] if x['id'] == sid), None)
    if not s:
        return {'status': 'error', 'message': 'Student not found'}, 404
    records = [r for r in db['attendance_records'] if r['student_id'] == sid]
    return {'status': 'success', 'data': records, 'meta': {'total': len(records)}}


@students_bp.route('/<int:sid>', methods=['PUT'])
@role_required('admin', 'faculty')
def update_student(sid, current_user_id, current_role):
    s = next((x for x in db['students'] if x['id'] == sid), None)
    if not s:
        return {'status': 'error', 'message': 'Student not found'}, 404
    data = request.get_json(silent=True) or {}
    for key in ('first_name', 'last_name', 'roll_number', 'class_id', 'section', 'department', 'enrollment_status', 'is_active'):
        if key in data:
            s[key] = data[key]
    return {'status': 'success', 'message': 'Student updated', 'data': _student_summary(s)}


@students_bp.route('/<int:sid>', methods=['DELETE'])
@role_required('admin')
def delete_student(sid, current_user_id, current_role):
    idx = next((i for i, x in enumerate(db['students']) if x['id'] == sid), None)
    if idx is None:
        return {'status': 'error', 'message': 'Student not found'}, 404
    db['students'].pop(idx)
    return {'status': 'success', 'message': 'Student deleted'}

@students_bp.route('/my-dashboard', methods=['GET'])
@role_required('student')
def my_dashboard(current_user_id, current_role):
    student = next((s for s in db['students'] if s['student_id'] == current_user_id), None)
    if not student:
        return {'status': 'error', 'message': 'Student profile not found'}, 404
    records = [r for r in db['attendance_records'] if r['student_id'] == student['id']]
    present = sum(1 for r in records if r['status'] in ('PRESENT', 'LATE'))
    total = len(records)
    rate = round(present / total * 100, 1) if total > 0 else 0
    # Subject-wise breakdown
    subjects = []
    for sub in db['subjects']:
        session_ids = {s['id'] for s in db['attendance_sessions'] if s['subject_id'] == sub['id']}
        sub_records = [r for r in records if r['session_id'] in session_ids]
        if sub_records:
            s_present = sum(1 for r in sub_records if r['status'] in ('PRESENT', 'LATE'))
            s_total = len(sub_records)
            subjects.append({'name': sub['name'], 'code': sub['code'], 'present': s_present, 'total': s_total, 'percentage': round(s_present / s_total * 100, 1) if s_total > 0 else 0})
    return {'status': 'success', 'data': {'student': {**student, 'full_name': f"{student['first_name']} {student['last_name']}"}, 'overall': {'present': present, 'absent': total - present, 'total': total, 'percentage': rate}, 'subjects': subjects}}
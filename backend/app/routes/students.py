"""Student Routes"""
from flask import Blueprint, request
from app.db import session_scope
from app.models.student import ParentGuardian, Student
from app.models.qr import QRIdentity
from app.models.attendance import AttendanceRecord, AttendanceSession
from app.models.subject import Subject
from app.utils.jwt_utils import auth_required, role_required
import uuid

students_bp = Blueprint('students', __name__)


def _student_summary(s, session):
    parent = session.query(ParentGuardian).filter_by(student_id=s.id).first()
    qr = session.query(QRIdentity).filter_by(student_id=s.id).first()
    records = session.query(AttendanceRecord).filter_by(student_id=s.id).all()
    present = sum(1 for r in records if r.status in ('PRESENT', 'LATE'))
    return {
        **s.to_dict(),
        'parent': bool(parent),
        'qr': bool(qr and qr.is_active),
        'overall_attendance': round(present / len(records) * 100, 1) if records else 0.0,
    }


@students_bp.route('/', methods=['GET'])
@auth_required
def get_students(current_user_id, current_role):
    with session_scope() as s:
        students = s.query(Student).filter_by(is_active=True).all()
        data = [_student_summary(st, s) for st in students]
        return {'status': 'success', 'data': data, 'meta': {'total': len(data)}}


@students_bp.route('/<int:sid>', methods=['GET'])
@auth_required
def get_student(sid, current_user_id, current_role):
    with session_scope() as s:
        st = s.query(Student).filter_by(id=sid).first()
        if not st:
            return {'status': 'error', 'message': 'Student not found'}, 404
        return {'status': 'success', 'data': _student_summary(st, s)}


@students_bp.route('/', methods=['POST'])
@role_required('admin', 'faculty')
def create_student(current_user_id, current_role):
    data = request.get_json(silent=True) or {}
    first_name = (data.get('first_name') or '').strip()
    last_name = (data.get('last_name') or '').strip()
    if not first_name or not last_name:
        return {'status': 'error', 'message': 'first_name and last_name are required'}, 400

    with session_scope() as s:
        count = s.query(Student).count()
        student = Student(
            student_id=f'STU{count + 1:04d}', first_name=first_name, last_name=last_name,
            roll_number=data.get('roll_number') or f'42{count + 1:02d}',
            class_id=data.get('class_id', 1), section=data.get('section', 'A'),
            department=data.get('department', 'CSE'), enrollment_status='incomplete', is_active=True,
        )
        s.add(student)
        s.flush()
        s.add(ParentGuardian(
            student_id=student.id, name=data.get('parent_name') or f'Mr. {last_name}',
            whatsapp_number=data.get('parent_whatsapp') or f'+9198765{count + 1:05d}', relationship='father',
        ))
        s.add(QRIdentity(student_id=student.id, qr_identifier=f'QR{uuid.uuid4().hex[:8].upper()}', is_active=True))
        s.flush()
        return {'status': 'success', 'message': 'Student created', 'data': _student_summary(student, s)}, 201


@students_bp.route('/<int:sid>/attendance', methods=['GET'])
@auth_required
def student_attendance(sid, current_user_id, current_role):
    with session_scope() as s:
        st = s.query(Student).filter_by(id=sid).first()
        if not st:
            return {'status': 'error', 'message': 'Student not found'}, 404
        records = s.query(AttendanceRecord).filter_by(student_id=sid).all()
        return {'status': 'success', 'data': [r.to_dict() for r in records], 'meta': {'total': len(records)}}


@students_bp.route('/<int:sid>', methods=['PUT'])
@role_required('admin', 'faculty')
def update_student(sid, current_user_id, current_role):
    data = request.get_json(silent=True) or {}
    with session_scope() as s:
        st = s.query(Student).filter_by(id=sid).first()
        if not st:
            return {'status': 'error', 'message': 'Student not found'}, 404
        for key in ('first_name', 'last_name', 'roll_number', 'class_id', 'section', 'department', 'enrollment_status', 'is_active'):
            if key in data:
                setattr(st, key, data[key])
        s.flush()
        return {'status': 'success', 'message': 'Student updated', 'data': _student_summary(st, s)}


@students_bp.route('/<int:sid>', methods=['DELETE'])
@role_required('admin')
def delete_student(sid, current_user_id, current_role):
    with session_scope() as s:
        st = s.query(Student).filter_by(id=sid).first()
        if not st:
            return {'status': 'error', 'message': 'Student not found'}, 404
        st.is_active = False
        s.flush()
        return {'status': 'success', 'message': 'Student deleted'}


@students_bp.route('/my-dashboard', methods=['GET'])
@role_required('student')
def my_dashboard(current_user_id, current_role):
    with session_scope() as s:
        student = s.query(Student).filter_by(student_id=current_user_id).first()
        if not student:
            return {'status': 'error', 'message': 'Student profile not found'}, 404
        records = s.query(AttendanceRecord).filter_by(student_id=student.id).all()
        present = sum(1 for r in records if r.status in ('PRESENT', 'LATE'))
        total = len(records)
        rate = round(present / total * 100, 1) if total > 0 else 0

        subjects = []
        for sub in s.query(Subject).all():
            session_ids = {x.id for x in s.query(AttendanceSession).filter_by(subject_id=sub.id).all()}
            sub_records = [r for r in records if r.session_id in session_ids]
            if sub_records:
                s_present = sum(1 for r in sub_records if r.status in ('PRESENT', 'LATE'))
                s_total = len(sub_records)
                subjects.append({'name': sub.name, 'code': sub.code, 'present': s_present, 'total': s_total, 'percentage': round(s_present / s_total * 100, 1) if s_total > 0 else 0})
        return {'status': 'success', 'data': {'student': student.to_dict(), 'overall': {'present': present, 'absent': total - present, 'total': total, 'percentage': rate}, 'subjects': subjects}}

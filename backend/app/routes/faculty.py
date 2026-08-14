"""Faculty Routes"""
from flask import Blueprint, request
from app.db import session_scope
from app.models.attendance import AttendanceRecord, AttendanceSession
from app.models.class_ import ClassModel
from app.models.student import ParentGuardian, Student
from app.models.subject import Subject
from app.models.qr import QRIdentity
from app.utils.jwt_utils import role_required
from datetime import date

faculty_bp = Blueprint('faculty', __name__)


@faculty_bp.route('/dashboard', methods=['GET'])
@role_required('faculty', 'admin')
def get_dashboard(current_user_id, current_role):
    today = date.today()
    with session_scope() as s:
        sessions = s.query(AttendanceSession).filter_by(scheduled_date=today).all()
        records = s.query(AttendanceRecord).filter_by(attendance_date=today).all()
        total = len(records)
        present = sum(1 for r in records if r.status in ('PRESENT', 'LATE'))

        session_list = []
        for sess in sessions:
            subject = s.query(Subject).filter_by(id=sess.subject_id).first()
            cls = s.query(ClassModel).filter_by(id=sess.class_id).first()
            session_list.append({
                'id': sess.id, 'session_id': sess.session_id,
                'subject_name': subject.name if subject else 'Unknown',
                'class_name': f"{cls.code}-A" if cls else 'Unknown',
                'time': sess.scheduled_date.isoformat() if sess.scheduled_date else None,
                'status': sess.status, 'mode': sess.attendance_mode,
            })
        return {
            'status': 'success',
            'data': {
                'today_date': today.isoformat(),
                'today_sessions': session_list,
                'today_total': total, 'today_present': present, 'today_absent': total - present,
                'attendance_rate': round(present / total * 100, 1) if total > 0 else 0,
            }
        }


@faculty_bp.route('/schedule', methods=['GET'])
@role_required('faculty', 'admin')
def get_schedule(current_user_id, current_role):
    today = date.today()
    with session_scope() as s:
        sessions = s.query(AttendanceSession).filter_by(scheduled_date=today).all()
        result = []
        for sess in sessions:
            subject = s.query(Subject).filter_by(id=sess.subject_id).first()
            result.append({
                'id': sess.id, 'subject': subject.to_dict() if subject else None,
                'class_id': sess.class_id, 'attendance_mode': sess.attendance_mode,
                'status': sess.status, 'scheduled_date': sess.scheduled_date.isoformat() if sess.scheduled_date else None,
            })
        return {'status': 'success', 'data': result}


@faculty_bp.route('/students', methods=['GET'])
@role_required('faculty', 'admin')
def get_faculty_students(current_user_id, current_role):
    with session_scope() as s:
        students = []
        for st in s.query(Student).filter_by(is_active=True).all():
            parent = s.query(ParentGuardian).filter_by(student_id=st.id).first()
            qr = s.query(QRIdentity).filter_by(student_id=st.id).first()
            students.append({**st.to_dict(), 'parent': bool(parent),
                             'face': st.enrollment_status in ('ready', 'face_enrolled'),
                             'qr': bool(qr and qr.is_active)})
        return {'status': 'success', 'data': students}


@faculty_bp.route('/students/<int:sid>/enroll-face', methods=['POST'])
@role_required('faculty', 'admin')
def enroll_face(sid, current_user_id, current_role):
    with session_scope() as s:
        st = s.query(Student).filter_by(id=sid).first()
        if not st:
            return {'status': 'error', 'message': 'Student not found'}, 404
        st.enrollment_status = 'face_enrolled'
        s.flush()
        return {'status': 'success', 'message': f'Face enrolled for {st.first_name}', 'data': {'student_id': sid, 'status': 'face_enrolled'}}

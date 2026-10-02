"""Attendance Routes"""
from flask import Blueprint, request
from app.db import session_scope
from app.models.attendance import AttendanceRecord, AttendanceSession
from app.models.class_ import ClassModel
from app.models.notification import NotificationQueue
from app.models.student import ParentGuardian, Student
from app.models.subject import Subject
from app.utils.jwt_utils import role_required
from datetime import date, datetime
import uuid

attendance_bp = Blueprint('attendance', __name__)


@attendance_bp.route('/sessions', methods=['GET'])
@role_required('faculty', 'admin')
def get_sessions(current_user_id, current_role):
    with session_scope() as s:
        sessions = []
        for sess in s.query(AttendanceSession).all():
            subject = s.query(Subject).filter_by(id=sess.subject_id).first()
            cls = s.query(ClassModel).filter_by(id=sess.class_id).first()
            marked = s.query(AttendanceRecord).filter_by(session_id=sess.id).count()
            sessions.append({
                **sess.to_dict(),
                'subject_name': subject.name if subject else None,
                'class_name': cls.name if cls else None,
                'marked': marked,
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

    with session_scope() as s:
        total = s.query(Student).filter_by(class_id=int(class_id), is_active=True).count()
        sched = data.get('scheduled_date')
        scheduled_date = date.fromisoformat(sched) if sched else date.today()
        sess = AttendanceSession(
            session_id=f'SES{uuid.uuid4().hex[:8].upper()}', subject_id=int(subject_id),
            class_id=int(class_id), faculty_id=data.get('faculty_id', 1),
            attendance_mode=(data.get('mode') or data.get('attendance_mode') or 'FACE').upper(),
            status='active', total_students=total, scheduled_date=scheduled_date, created_at=datetime.utcnow(),
        )
        s.add(sess)
        s.flush()
        return {'status': 'success', 'message': 'Session created', 'data': sess.to_dict()}, 201


@attendance_bp.route('/sessions/<int:sid>', methods=['GET'])
@role_required('faculty', 'admin', 'student')
def get_session(sid, current_user_id, current_role):
    with session_scope() as s:
        sess = s.query(AttendanceSession).filter_by(id=sid).first()
        if not sess:
            return {'status': 'error', 'message': 'Session not found'}, 404
        records = s.query(AttendanceRecord).filter_by(session_id=sid).all()
        subject = s.query(Subject).filter_by(id=sess.subject_id).first()
        cls = s.query(ClassModel).filter_by(id=sess.class_id).first()
        return {
            'status': 'success',
            'data': {
                **sess.to_dict(),
                'subject_name': subject.name if subject else None,
                'class_name': cls.name if cls else None,
                'class_code': cls.code if cls else None,
                'records': [r.to_dict() for r in records],
                'present': sum(1 for r in records if r.status in ('PRESENT', 'LATE')),
            }
        }


@attendance_bp.route('/sessions/<int:sid>/mark', methods=['POST'])
@role_required('faculty', 'admin')
def mark_attendance(sid, current_user_id, current_role):
    data = request.get_json(silent=True) or {}
    student_id = data.get('student_id') or data.get('student')
    if not student_id:
        return {'status': 'error', 'message': 'student_id is required'}, 400
    student_id = int(student_id)

    with session_scope() as s:
        sess = s.query(AttendanceSession).filter_by(id=sid).first()
        if not sess:
            return {'status': 'error', 'message': 'Session not found'}, 404
        if s.query(AttendanceRecord).filter_by(student_id=student_id, session_id=sid).first():
            return {'status': 'error', 'message': 'Attendance already marked for this student'}, 400

        record = AttendanceRecord(
            student_id=student_id, session_id=sid,
            status=(data.get('status') or 'PRESENT').upper(),
            attendance_method=(data.get('method') or data.get('attendance_method') or 'FACE').upper(),
            attendance_date=date.today(), created_at=datetime.utcnow(),
        )
        s.add(record)

        student = s.query(Student).filter_by(id=student_id).first()
        if student:
            parent = s.query(ParentGuardian).filter_by(student_id=student_id).first()
            if parent:
                s.add(NotificationQueue(
                    session_id=sid, recipient_number=parent.whatsapp_number,
                    message=f"Attendance marked for {student.first_name} {student.last_name}",
                    status='SENT', created_at=datetime.utcnow().isoformat(),
                ))
        s.flush()
        return {'status': 'success', 'message': 'Attendance marked', 'data': record.to_dict()}, 201


@attendance_bp.route('/sessions/<int:sid>/start', methods=['POST'])
@role_required('faculty', 'admin')
def start_session(sid, current_user_id, current_role):
    with session_scope() as s:
        sess = s.query(AttendanceSession).filter_by(id=sid).first()
        if not sess:
            return {'status': 'error', 'message': 'Session not found'}, 404
        sess.status = 'active'
        s.flush()
        return {'status': 'success', 'message': 'Session started', 'data': sess.to_dict()}


@attendance_bp.route('/sessions/<int:sid>/end', methods=['POST'])
@role_required('faculty', 'admin')
def end_session(sid, current_user_id, current_role):
    with session_scope() as s:
        sess = s.query(AttendanceSession).filter_by(id=sid).first()
        if not sess:
            return {'status': 'error', 'message': 'Session not found'}, 404
        sess.status = 'completed'
        s.flush()
        return {'status': 'success', 'message': 'Session ended', 'data': sess.to_dict()}


@attendance_bp.route('/sessions/<int:sid>/batch-mark', methods=['POST'])
@role_required('faculty', 'admin')
def batch_mark(sid, current_user_id, current_role):
    data = request.get_json(silent=True) or {}
    records = data.get('records', [])
    with session_scope() as s:
        sess = s.query(AttendanceSession).filter_by(id=sid).first()
        if not sess:
            return {'status': 'error', 'message': 'Session not found'}, 404
        created = []
        for rec in records:
            student_id = int(rec.get('student_id'))
            status = (rec.get('status') or 'PRESENT').upper()
            if s.query(AttendanceRecord).filter_by(student_id=student_id, session_id=sid).first():
                continue
            record = AttendanceRecord(
                student_id=student_id, session_id=sid, status=status,
                attendance_method=(rec.get('method') or 'MANUAL').upper(),
                attendance_date=date.today(), created_at=datetime.utcnow(),
            )
            s.add(record)
            s.flush()
            created.append(record.to_dict())
        return {'status': 'success', 'message': f'{len(created)} records created', 'data': created}


@attendance_bp.route('/my-attendance', methods=['GET'])
@role_required('student')
def my_attendance(current_user_id, current_role):
    with session_scope() as s:
        student = s.query(Student).filter_by(student_id=current_user_id).first()
        if not student:
            return {'status': 'error', 'message': 'Student not found'}, 404
        enriched = []
        for r in s.query(AttendanceRecord).filter_by(student_id=student.id).all():
            sess = s.query(AttendanceSession).filter_by(id=r.session_id).first()
            subject = s.query(Subject).filter_by(id=sess.subject_id).first() if sess else None
            enriched.append({**r.to_dict(), 'subject_name': subject.name if subject else None,
                             'subject_code': subject.code if subject else None})
        return {'status': 'success', 'data': enriched}

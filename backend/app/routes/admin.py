"""Admin Routes"""
from flask import Blueprint, request
from app.db import session_scope
from app.models.attendance import AttendanceRecord, AttendanceSession
from app.models.class_ import ClassModel
from app.models.faculty import Faculty
from app.models.notification import NotificationQueue
from app.models.student import Student
from app.models.subject import Subject
from app.models.user import User
from app.utils.jwt_utils import role_required
from datetime import date

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/dashboard', methods=['GET'])
@role_required('admin')
def get_dashboard(current_user_id, current_role):
    today = date.today()
    with session_scope() as s:
        today_records = s.query(AttendanceRecord).filter_by(attendance_date=today).all()
        today_attendance = len(today_records)
        today_present = sum(1 for r in today_records if r.status in ('PRESENT', 'LATE'))
        avg_attendance = round(today_present / today_attendance * 100, 1) if today_attendance > 0 else 0

        low_attendance = s.query(Student).filter(
            Student.is_active == True,  # noqa: E712
            Student.enrollment_status.in_(['incomplete', 'face_required'])
        ).count()

        sent = s.query(NotificationQueue).filter_by(status='SENT').count()
        failed = s.query(NotificationQueue).filter_by(status='FAILED').count()

        return {
            'status': 'success',
            'data': {
                'total_students': s.query(Student).filter_by(is_active=True).count(),
                'total_faculty': s.query(Faculty).count(),
                'total_classes': s.query(ClassModel).filter_by(is_active=True).count(),
                'total_subjects': s.query(Subject).filter_by(is_active=True).count(),
                'today_attendance': today_attendance,
                'today_present': today_present,
                'avg_attendance': avg_attendance,
                'low_attendance_count': low_attendance,
                'whatsapp_sent': sent,
                'whatsapp_failed': failed,
            }
        }


@admin_bp.route('/stats', methods=['GET'])
@role_required('admin')
def get_stats(current_user_id, current_role):
    with session_scope() as s:
        return {
            'status': 'success',
            'data': {
                'students': s.query(Student).count(),
                'faculty': s.query(Faculty).count(),
                'classes': s.query(ClassModel).count(),
                'subjects': s.query(Subject).count(),
                'sessions': s.query(AttendanceSession).count(),
                'records': s.query(AttendanceRecord).count(),
                'notifications': s.query(NotificationQueue).count(),
            }
        }


@admin_bp.route('/faculty', methods=['GET'])
@role_required('admin')
def get_faculty(current_user_id, current_role):
    with session_scope() as s:
        faculty = []
        for f in s.query(Faculty).filter_by(is_active=True).all():
            user = s.query(User).filter_by(id=f.user_id).first() if f.user_id else None
            faculty.append({
                **f.to_dict(),
                'email': user.email if user else None,
                'is_active': user.is_active if user else f.is_active,
            })
        return {'status': 'success', 'data': faculty, 'meta': {'total': len(faculty)}}


@admin_bp.route('/faculty/<int:fid>', methods=['DELETE'])
@role_required('admin')
def delete_faculty(fid, current_user_id, current_role):
    with session_scope() as s:
        f = s.query(Faculty).filter_by(id=fid).first()
        if not f:
            return {'status': 'error', 'message': 'Faculty not found'}, 404
        f.is_active = False
        if f.user_id:
            user = s.query(User).filter_by(id=f.user_id).first()
            if user:
                user.is_active = False
        s.flush()
        return {'status': 'success', 'message': 'Faculty deleted'}


@admin_bp.route('/faculty/<int:fid>', methods=['PUT'])
@role_required('admin')
def update_faculty(fid, current_user_id, current_role):
    data = request.get_json(silent=True) or {}
    with session_scope() as s:
        f = s.query(Faculty).filter_by(id=fid).first()
        if not f:
            return {'status': 'error', 'message': 'Faculty not found'}, 404
        for key in ('first_name', 'last_name', 'department', 'is_active'):
            if key in data:
                setattr(f, key, data[key])
        if 'is_active' in data and f.user_id:
            user = s.query(User).filter_by(id=f.user_id).first()
            if user:
                user.is_active = data['is_active']
        s.flush()
        user = s.query(User).filter_by(id=f.user_id).first() if f.user_id else None
        return {'status': 'success', 'message': 'Faculty updated', 'data': {**f.to_dict(), 'email': user.email if user else None, 'is_active': user.is_active if user else f.is_active}}

"""Admin Routes"""
from flask import Blueprint
from app.db import session_scope
from app.models.attendance import AttendanceRecord, AttendanceSession
from app.models.class_ import ClassModel
from app.models.faculty import Faculty
from app.models.notification import NotificationQueue
from app.models.student import Student
from app.models.subject import Subject
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

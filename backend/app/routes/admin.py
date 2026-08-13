"""Admin Routes"""
from flask import Blueprint
from app.store import db
from app.utils.jwt_utils import role_required
from datetime import date

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/dashboard', methods=['GET'])
@role_required('admin')
def get_dashboard(current_user_id, current_role):
    today = date.today().isoformat()
    today_records = [r for r in db['attendance_records'] if r.get('attendance_date') == today]
    today_attendance = len(today_records)
    today_present = sum(1 for r in today_records if r['status'] in ('PRESENT', 'LATE'))
    avg_attendance = round(today_present / today_attendance * 100, 1) if today_attendance > 0 else 0

    low_attendance = sum(
        1 for s in db['students']
        if s.get('enrollment_status') in ('incomplete', 'face_required') and s.get('is_active', True)
    )

    sent = sum(1 for n in db['notification_queue'] if n['status'] == 'SENT')
    failed = sum(1 for n in db['notification_queue'] if n['status'] == 'FAILED')

    return {
        'status': 'success',
        'data': {
            'total_students': len([s for s in db['students'] if s.get('is_active', True)]),
            'total_faculty': len(db['faculty']),
            'total_classes': len(db['classes']),
            'total_subjects': len(db['subjects']),
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
    return {
        'status': 'success',
        'data': {
            'students': len(db['students']),
            'faculty': len(db['faculty']),
            'classes': len(db['classes']),
            'subjects': len(db['subjects']),
            'sessions': len(db['attendance_sessions']),
            'records': len(db['attendance_records']),
            'notifications': len(db['notification_queue']),
        }
    }

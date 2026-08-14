"""Reports Routes"""
from flask import Blueprint, request
from app.db import session_scope
from app.models.attendance import AttendanceRecord, AttendanceSession
from app.models.student import Student
from app.models.subject import Subject
from app.utils.jwt_utils import auth_required
from datetime import datetime

reports_bp = Blueprint('reports', __name__)


def _rate(records):
    total = len(records)
    present = sum(1 for r in records if r.status in ('PRESENT', 'LATE'))
    return total, present, (round(present / total * 100, 1) if total > 0 else 0)


@reports_bp.route('/daily', methods=['GET'])
@auth_required
def daily_report(current_user_id, current_role):
    date_str = request.args.get('date')
    report_date = datetime.fromisoformat(date_str).date() if date_str else datetime.utcnow().date()
    with session_scope() as s:
        records = s.query(AttendanceRecord).filter_by(attendance_date=report_date).all()
        total, present, rate = _rate(records)
        return {
            'status': 'success', 'message': 'Daily report generated',
            'data': {'report_date': report_date.isoformat(), 'total': total, 'present': present,
                     'absent': total - present, 'rate': rate}
        }


@reports_bp.route('/weekly', methods=['GET'])
@auth_required
def weekly_report(current_user_id, current_role):
    with session_scope() as s:
        records = s.query(AttendanceRecord).all()
        total, present, rate = _rate(records)
        return {
            'status': 'success', 'message': 'Weekly report generated',
            'data': {'total': total, 'present': present, 'absent': total - present, 'rate': rate}
        }


@reports_bp.route('/monthly', methods=['GET'])
@auth_required
def monthly_report(current_user_id, current_role):
    with session_scope() as s:
        records = s.query(AttendanceRecord).all()
        total, present, rate = _rate(records)
        subjects = []
        for sub in s.query(Subject).all():
            session_ids = {x.id for x in s.query(AttendanceSession).filter_by(subject_id=sub.id).all()}
            subject_records = [r for r in records if r.session_id in session_ids]
            if subject_records:
                _, _, s_rate = _rate(subject_records)
                subjects.append({'code': sub.code, 'name': sub.name, 'percentage': s_rate})
        student = s.query(Student).first()
        return {
            'status': 'success', 'message': 'Monthly report generated',
            'data': {
                'student_name': f"{student.first_name} {student.last_name}" if student else '—',
                'summary': {'percentage': rate, 'present': present, 'absent': total - present},
                'subjects': subjects,
            }
        }


@reports_bp.route('/student/<int:sid>', methods=['GET'])
@auth_required
def student_report(sid, current_user_id, current_role):
    with session_scope() as s:
        student = s.query(Student).filter_by(id=sid).first()
        if not student:
            return {'status': 'error', 'message': 'Student not found'}, 404
        records = s.query(AttendanceRecord).filter_by(student_id=sid).all()
        total, present, rate = _rate(records)
        return {
            'status': 'success',
            'data': {
                'student_name': f"{student.first_name} {student.last_name}",
                'student_id': student.student_id, 'total_classes': total,
                'present': present, 'absent': total - present, 'overall_rate': rate,
            }
        }

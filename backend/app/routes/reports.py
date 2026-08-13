"""Reports Routes"""
from flask import Blueprint, request
from app.store import db
from app.utils.jwt_utils import auth_required
from datetime import datetime

reports_bp = Blueprint('reports', __name__)


def _rate(records):
    total = len(records)
    present = sum(1 for r in records if r['status'] in ('PRESENT', 'LATE'))
    return total, present, (round(present / total * 100, 1) if total > 0 else 0)


@reports_bp.route('/daily', methods=['GET'])
@auth_required
def daily_report(current_user_id, current_role):
    date_str = request.args.get('date')
    report_date = date_str if date_str else datetime.utcnow().date().isoformat()
    records = [r for r in db['attendance_records'] if r.get('attendance_date') == report_date]
    total, present, rate = _rate(records)
    return {
        'status': 'success',
        'message': 'Daily report generated',
        'data': {
            'report_date': report_date,
            'total': total,
            'present': present,
            'absent': total - present,
            'rate': rate,
        }
    }


@reports_bp.route('/weekly', methods=['GET'])
@auth_required
def weekly_report(current_user_id, current_role):
    records = db['attendance_records']
    total, present, rate = _rate(records)
    return {
        'status': 'success',
        'message': 'Weekly report generated',
        'data': {'total': total, 'present': present, 'absent': total - present, 'rate': rate}
    }


@reports_bp.route('/monthly', methods=['GET'])
@auth_required
def monthly_report(current_user_id, current_role):
    records = db['attendance_records']
    total, present, rate = _rate(records)

    # Group records by subject through their session
    subjects = []
    for sub in db['subjects']:
        session_ids = {s['id'] for s in db['attendance_sessions'] if s['subject_id'] == sub['id']}
        subject_records = [r for r in records if r['session_id'] in session_ids]
        s_total, s_present, s_rate = _rate(subject_records)
        if s_total:
            subjects.append({'code': sub['code'], 'name': sub['name'], 'percentage': s_rate})

    student = next((s for s in db['students']), None)
    return {
        'status': 'success',
        'message': 'Monthly report generated',
        'data': {
            'student_name': f"{student['first_name']} {student['last_name']}" if student else '—',
            'summary': {'percentage': rate, 'present': present, 'absent': total - present},
            'subjects': subjects,
        }
    }


@reports_bp.route('/student/<int:sid>', methods=['GET'])
@auth_required
def student_report(sid, current_user_id, current_role):
    student = next((s for s in db['students'] if s['id'] == sid), None)
    if not student:
        return {'status': 'error', 'message': 'Student not found'}, 404
    records = [r for r in db['attendance_records'] if r['student_id'] == sid]
    total, present, rate = _rate(records)
    return {
        'status': 'success',
        'data': {
            'student_name': f"{student['first_name']} {student['last_name']}",
            'student_id': student['student_id'],
            'total_classes': total,
            'present': present,
            'absent': total - present,
            'overall_rate': rate,
        }
    }

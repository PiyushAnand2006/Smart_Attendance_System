"""Face Recognition Routes (mock mode)

The full pipeline would integrate a face-recognition library. This enrollment /
verification keeps the API contract stable without heavy dependencies while
persisting enrollment status to the database.
"""
from flask import Blueprint, request
from app.db import session_scope
from app.models.student import Student
from app.utils.jwt_utils import role_required

face_bp = Blueprint('face', __name__)


@face_bp.route('/enroll', methods=['POST'])
@role_required('faculty', 'admin')
def enroll(current_user_id, current_role):
    data = request.get_json(silent=True) or {}
    student_id = data.get('student_id')
    if not student_id:
        return {'status': 'error', 'message': 'student_id is required'}, 400
    with session_scope() as s:
        student = s.query(Student).filter_by(id=int(student_id)).first()
        if not student:
            return {'status': 'error', 'message': 'Student not found'}, 404
        student.enrollment_status = 'face_enrolled'
        s.flush()
        return {'status': 'success', 'message': 'Face enrolled', 'data': {'student_id': student.id}}


@face_bp.route('/verify', methods=['POST'])
@role_required('faculty', 'admin')
def verify(current_user_id, current_role):
    data = request.get_json(silent=True) or {}
    student_id = data.get('student_id')
    with session_scope() as s:
        student = s.query(Student).filter_by(id=int(student_id or 0)).first()
        if not student:
            return {'status': 'error', 'message': 'Student not found'}, 404
        return {'status': 'success', 'data': {'student_id': student.id, 'verified': True, 'confidence': 0.97}}

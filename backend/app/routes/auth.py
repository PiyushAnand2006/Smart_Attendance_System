"""Authentication Routes"""
from flask import Blueprint, request
from app.db import session_scope
from app.models.user import User
from app.models.student import Student, ParentGuardian
from app.models.faculty import Faculty
from app.models.qr import QRIdentity
from app.store import hash_pwd
from app.utils.jwt_utils import create_access_token, create_refresh_token, auth_required
import uuid

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json(silent=True) or {}
    email = (data.get('email') or '').strip().lower()
    password = data.get('password') or ''
    selected_role = (data.get('role') or '').strip().lower()

    with session_scope() as s:
        user = s.query(User).filter_by(email=email).first()
        if not user or user.password != hash_pwd(password):
            return {'status': 'error', 'message': 'Invalid email or password'}, 401
        if not user.is_active:
            return {'status': 'error', 'message': 'Account is disabled'}, 403
        if selected_role and selected_role != user.role:
            return {'status': 'error', 'message': f'Account is not a {selected_role}'}, 403

        token = create_access_token(user.user_id, user.role)
        return {
            'status': 'success',
            'data': {
                'access_token': token,
                'refresh_token': create_refresh_token(user.user_id),
                'user': user.to_dict(),
                'role': user.role,
            }
        }


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json(silent=True) or {}
    email = (data.get('email') or '').strip().lower()
    password = data.get('password') or ''
    first_name = (data.get('first_name') or '').strip()
    last_name = (data.get('last_name') or '').strip()
    role = data.get('role') or 'student'

    if role not in ('student', 'faculty'):
        return {'status': 'error', 'message': 'Invalid role'}, 400
    if not email or not password:
        return {'status': 'error', 'message': 'Email and password are required'}, 400
    if len(password) < 6:
        return {'status': 'error', 'message': 'Password must be at least 6 characters'}, 400

    with session_scope() as s:
        if s.query(User).filter_by(email=email).first():
            return {'status': 'error', 'message': 'Email already registered'}, 400

        user = User(
            user_id=f'USR{uuid.uuid4().hex[:8].upper()}', email=email,
            password=hash_pwd(password), first_name=first_name, last_name=last_name,
            role=role, is_active=True,
        )
        s.add(user)
        s.flush()

        # Make the registration functional: provision the role-specific profile.
        if role == 'student':
            student = Student(
                student_id=f'STU{uuid.uuid4().hex[:6].upper()}', first_name=first_name,
                last_name=last_name, enrollment_status='incomplete', is_active=True,
            )
            s.add(student)
            s.flush()
            s.add(ParentGuardian(student_id=student.id, name=f'Mr. {last_name}', relationship='father'))
            s.add(QRIdentity(student_id=student.id, qr_identifier=f'QR{uuid.uuid4().hex[:8].upper()}', is_active=True))
            user.user_id = student.student_id
        elif role == 'faculty':
            faculty = Faculty(faculty_id=f'FAC{uuid.uuid4().hex[:6].upper()}', user_id=user.id,
                              first_name=first_name, last_name=last_name, is_active=True)
            s.add(faculty)
            s.flush()
            user.user_id = faculty.faculty_id

        token = create_access_token(user.user_id, user.role)
        return {
            'status': 'success',
            'message': 'Account created',
            'data': {
                'access_token': token,
                'user': user.to_dict(),
                'role': user.role,
            }
        }, 201


@auth_bp.route('/me', methods=['GET'])
@auth_required
def me(current_user_id, current_role):
    with session_scope() as s:
        user = s.query(User).filter_by(user_id=current_user_id).first()
        if not user:
            return {'status': 'error', 'message': 'User not found'}, 404
        return {'status': 'success', 'data': user.to_dict()}

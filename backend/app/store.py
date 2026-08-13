"""In-memory data store for the SmartAttend backend.

The full backend runs on Flask + PyJWT (no SQLAlchemy dependency required).
This module holds the shared in-memory dataset and demo seed data so the
application is usable out of the box.
"""
import hashlib
import uuid
from datetime import datetime

# ---------------------------------------------------------------------------
# Demo users
# ---------------------------------------------------------------------------
DEMO_USERS = [
    {'email': 'admin@smartattend.com', 'password': 'admin123', 'role': 'admin', 'first_name': 'System', 'last_name': 'Admin'},
    {'email': 'faculty@smartattend.com', 'password': 'faculty123', 'role': 'faculty', 'first_name': 'Dr. Rajesh', 'last_name': 'Kumar'},
    {'email': 'student@smartattend.com', 'password': 'student123', 'role': 'student', 'first_name': 'Rahul', 'last_name': 'Sharma'},
]

STUDENT_NAMES = [
    ('Rahul', 'Sharma'), ('Priya', 'Patil'), ('Amit', 'Kumar'), ('Sneha', 'Rao'),
    ('Vikram', 'Singh'), ('Ananya', 'Gupta'), ('Ravi', 'Reddy'), ('Kavya', 'Nair'),
    ('Arjun', 'Menon'), ('Divya', 'Iyer'), ('Suresh', 'Naidu'), ('Meera', 'Das'),
    ('Nikhil', 'Verma'), ('Pooja', 'Shetty'), ('Kiran', 'Bhat'),
]

SUBJECT_SEED = [
    ('Database Management Systems', 'DBMS'),
    ('Artificial Intelligence', 'AI'),
    ('Operating Systems', 'OS'),
    ('Computer Networks', 'CN'),
]

TEMPLATE_SEED = [
    ('present', 'Present', 'Dear {{parent_name}}, {{student_name}} attendance recorded.'),
    ('late', 'Late', 'Dear {{parent_name}}, {{student_name}} arrived late.'),
    ('absent', 'Absent', 'Dear {{parent_name}}, {{student_name}} was absent.'),
    ('warning', 'Warning', 'Dear {{parent_name}}, attendance low.'),
]


def hash_pwd(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def _seed():
    """Populate the store with demo data (idempotent)."""
    if db['users']:
        return

    # Users
    for i, u in enumerate(DEMO_USERS, 1):
        db['users'].append({
            'id': i,
            'user_id': ('ADM001' if u['role'] == 'admin' else 'FAC001' if u['role'] == 'faculty' else 'STU001'),
            'email': u['email'],
            'password': hash_pwd(u['password']),
            'first_name': u['first_name'],
            'last_name': u['last_name'],
            'role': u['role'],
            'is_active': True,
        })

    # Faculty
    db['faculty'].append({
        'id': 1, 'faculty_id': 'FAC1001', 'user_id': 2,
        'first_name': 'Dr. Rajesh', 'last_name': 'Kumar',
        'department': 'Computer Science',
    })

    # Classes
    db['classes'].append({'id': 1, 'name': 'Computer Science', 'code': 'CSE', 'department': 'Engineering', 'batch_year': 2025})

    # Subjects
    for name, code in SUBJECT_SEED:
        db['subjects'].append({
            'id': len(db['subjects']) + 1, 'name': name, 'code': code,
            'credits': 3, 'department': 'CSE', 'semester': 1, 'is_active': True,
        })

    # Students + parents + QR identities
    for i, (first, last) in enumerate(STUDENT_NAMES, 1):
        db['students'].append({
            'id': i, 'student_id': f'STU{i:04d}',
            'first_name': first, 'last_name': last,
            'roll_number': f'42{i:02d}', 'class_id': 1, 'section': 'A',
            'department': 'CSE',
            'enrollment_status': 'ready' if i <= 2 else 'incomplete',
            'is_active': True,
        })
        db['parents'].append({
            'id': i, 'student_id': i,
            'name': f'Mr. {last}', 'whatsapp_number': f'+9198765{i:05d}',
            'relationship': 'father',
        })
        db['qr_identities'].append({
            'id': i, 'student_id': i,
            'qr_identifier': f'QR{uuid.uuid4().hex[:8].upper()}',
            'is_active': True,
        })

    # Notification templates
    for name, display_name, content in TEMPLATE_SEED:
        db['notification_templates'].append({
            'id': len(db['notification_templates']) + 1,
            'name': name, 'display_name': display_name,
            'content': content, 'is_active': True,
        })

    # A couple of attendance sessions & records so dashboards have data
    now = datetime.utcnow()
    session = {
        'id': 1, 'session_id': 'SES' + uuid.uuid4().hex[:8].upper(),
        'subject_id': 1, 'class_id': 1, 'faculty_id': 1,
        'attendance_mode': 'FACE', 'status': 'completed',
        'total_students': len(db['students']),
        'scheduled_date': now.date().isoformat(),
        'created_at': now.isoformat(),
    }
    db['attendance_sessions'].append(session)
    for i in range(1, 5):
        db['attendance_records'].append({
            'id': i, 'student_id': i, 'session_id': 1,
            'status': 'PRESENT', 'attendance_method': 'FACE',
            'attendance_date': now.date().isoformat(),
            'created_at': now.isoformat(),
        })
    db['notification_queue'].append({
        'id': 1, 'session_id': 1, 'recipient_number': '+919876500001',
        'message': 'Attendance marked for Rahul', 'status': 'SENT',
        'created_at': now.isoformat(),
    })


db = {
    'users': [], 'students': [], 'faculty': [], 'parents': [],
    'classes': [], 'subjects': [], 'attendance_sessions': [],
    'attendance_records': [], 'qr_identities': [],
    'notification_templates': [], 'notification_queue': [],
}

_seed()

"""Database seeding for the SmartAttend backend.

Idempotent: demo data is only inserted when the relevant tables are empty, so
the backend can be restarted safely without duplicating records.
"""
import hashlib
import uuid
from datetime import date, datetime

from app.models.attendance import AttendanceRecord, AttendanceSession
from app.models.class_ import ClassModel
from app.models.faculty import Faculty
from app.models.notification import NotificationQueue, NotificationTemplate
from app.models.qr import QRIdentity
from app.models.student import ParentGuardian, Student
from app.models.subject import Subject
from app.models.user import User

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


def seed_db(session):
    """Populate the database with demo data (idempotent)."""
    if session.query(User).count() > 0:
        return

    # Users
    users = {}
    for i, u in enumerate(DEMO_USERS, 1):
        user_id = 'ADM001' if u['role'] == 'admin' else 'FAC001' if u['role'] == 'faculty' else 'STU0001'
        user = User(
            user_id=user_id, email=u['email'], password=hash_pwd(u['password']),
            first_name=u['first_name'], last_name=u['last_name'], role=u['role'], is_active=True,
        )
        session.add(user)
        session.flush()
        users[u['role']] = user

    # Faculty
    faculty = Faculty(
        faculty_id='FAC1001', user_id=users['faculty'].id,
        first_name='Dr. Rajesh', last_name='Kumar', department='Computer Science', is_active=True,
    )
    session.add(faculty)
    session.flush()

    # Class
    cls = ClassModel(name='Computer Science', code='CSE', department='Engineering', batch_year=2025, is_active=True)
    session.add(cls)
    session.flush()

    # Subjects
    subjects = []
    for name, code in SUBJECT_SEED:
        subject = Subject(name=name, code=code, credits=3, department='CSE', semester=1, is_active=True)
        session.add(subject)
        subjects.append(subject)
    session.flush()

    # Students + parents + QR identities
    students = []
    for i, (first, last) in enumerate(STUDENT_NAMES, 1):
        student = Student(
            student_id=f'STU{i:04d}', first_name=first, last_name=last,
            roll_number=f'42{i:02d}', class_id=cls.id, section='A', department='CSE',
            enrollment_status='ready' if i <= 2 else 'incomplete', is_active=True,
        )
        session.add(student)
        session.flush()
        students.append(student)

        session.add(ParentGuardian(
            student_id=student.id, name=f'Mr. {last}',
            whatsapp_number=f'+9198765{i:05d}', relationship='father',
        ))
        session.add(QRIdentity(
            student_id=student.id, qr_identifier=f'QR{uuid.uuid4().hex[:8].upper()}', is_active=True,
        ))

    # Notification templates
    for name, display_name, content in TEMPLATE_SEED:
        session.add(NotificationTemplate(name=name, display_name=display_name, content=content, is_active=True))

    # A demo attendance session + records + a queued notification
    now = datetime.utcnow()
    session_obj = AttendanceSession(
        session_id='SES' + uuid.uuid4().hex[:8].upper(),
        subject_id=subjects[0].id, class_id=cls.id, faculty_id=faculty.id,
        attendance_mode='FACE', status='completed', total_students=len(students),
        scheduled_date=now.date(), created_at=now,
    )
    session.add(session_obj)
    session.flush()

    for i in range(1, 5):
        session.add(AttendanceRecord(
            student_id=students[i - 1].id, session_id=session_obj.id,
            status='PRESENT', attendance_method='FACE', attendance_date=now.date(), created_at=now,
        ))
    session.add(NotificationQueue(
        session_id=session_obj.id, recipient_number='+919876500001',
        message='Attendance marked for Rahul', status='SENT', created_at=now.isoformat(),
    ))
    session.flush()

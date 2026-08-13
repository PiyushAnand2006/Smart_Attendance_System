"""Attendance Models"""


class AttendanceSession:
    """A live attendance-taking session."""

    def __init__(self, id=None, session_id=None, subject_id=None, class_id=None,
                 faculty_id=None, attendance_mode='FACE', status='active',
                 total_students=0, scheduled_date=None, created_at=None):
        self.id = id
        self.session_id = session_id
        self.subject_id = subject_id
        self.class_id = class_id
        self.faculty_id = faculty_id
        self.attendance_mode = attendance_mode
        self.status = status
        self.total_students = total_students
        self.scheduled_date = scheduled_date
        self.created_at = created_at

    def to_dict(self):
        return {
            'id': self.id,
            'session_id': self.session_id,
            'subject_id': self.subject_id,
            'class_id': self.class_id,
            'faculty_id': self.faculty_id,
            'attendance_mode': self.attendance_mode,
            'status': self.status,
            'total_students': self.total_students,
            'scheduled_date': self.scheduled_date,
            'created_at': self.created_at,
        }


class AttendanceRecord:
    """A single student's attendance for a session."""

    def __init__(self, id=None, student_id=None, session_id=None, status='PRESENT',
                 attendance_method='FACE', attendance_date=None, created_at=None):
        self.id = id
        self.student_id = student_id
        self.session_id = session_id
        self.status = status
        self.attendance_method = attendance_method
        self.attendance_date = attendance_date
        self.created_at = created_at

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'session_id': self.session_id,
            'status': self.status,
            'attendance_method': self.attendance_method,
            'attendance_date': self.attendance_date,
            'created_at': self.created_at,
        }

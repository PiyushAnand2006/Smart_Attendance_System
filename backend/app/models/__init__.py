"""Models Package"""
from app.models.user import User
from app.models.student import Student, ParentGuardian
from app.models.faculty import Faculty
from app.models.class_ import ClassModel, Section
from app.models.subject import Subject, FacultySubject
from app.models.attendance import AttendanceSession, AttendanceRecord
from app.models.qr import QRIdentity, QRToken
from app.models.notification import NotificationTemplate, NotificationQueue, NotificationLog
from app.models.settings import AttendanceThreshold, AcademicYear, Timetable

__all__ = [
    'User',
    'Student',
    'ParentGuardian', 
    'Faculty',
    'ClassModel',
    'Section',
    'Subject',
    'FacultySubject',
    'AttendanceSession',
    'AttendanceRecord',
    'QRIdentity',
    'QRToken',
    'NotificationTemplate',
    'NotificationQueue',
    'NotificationLog',
    'AttendanceThreshold',
    'AcademicYear',
    'Timetable'
]
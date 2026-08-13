"""Settings Models"""


class AttendanceThreshold:
    """Attendance threshold settings."""

    def __init__(self, id=None, threshold_percentage=75.0, warning_percentage=80.0,
                 critical_percentage=70.0, period_type='overall', period_value=None,
                 department=None, is_active=True, created_at=None, updated_at=None):
        self.id = id
        self.threshold_percentage = threshold_percentage
        self.warning_percentage = warning_percentage
        self.critical_percentage = critical_percentage
        self.period_type = period_type
        self.period_value = period_value
        self.department = department
        self.is_active = is_active
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self):
        return {
            'id': self.id,
            'threshold_percentage': self.threshold_percentage,
            'warning_percentage': self.warning_percentage,
            'critical_percentage': self.critical_percentage,
            'period_type': self.period_type,
            'period_value': self.period_value,
            'department': self.department,
            'is_active': self.is_active,
        }


class AcademicYear:
    """Academic year settings."""

    def __init__(self, id=None, year=None, start_date=None, end_date=None,
                 is_current=False, term_1_start=None, term_1_end=None,
                 term_2_start=None, term_2_end=None, created_at=None):
        self.id = id
        self.year = year
        self.start_date = start_date
        self.end_date = end_date
        self.is_current = is_current
        self.term_1_start = term_1_start
        self.term_1_end = term_1_end
        self.term_2_start = term_2_start
        self.term_2_end = term_2_end
        self.created_at = created_at

    def to_dict(self):
        return {
            'id': self.id,
            'year': self.year,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'is_current': self.is_current,
        }


class Timetable:
    """Class timetable entry."""

    def __init__(self, id=None, class_id=None, section_id=None, subject_id=None,
                 faculty_id=None, day_of_week=0, start_time=None, end_time=None,
                 room=None, is_active=True):
        self.id = id
        self.class_id = class_id
        self.section_id = section_id
        self.subject_id = subject_id
        self.faculty_id = faculty_id
        self.day_of_week = day_of_week
        self.start_time = start_time
        self.end_time = end_time
        self.room = room
        self.is_active = is_active

    def to_dict(self):
        return {
            'id': self.id,
            'class_id': self.class_id,
            'section_id': self.section_id,
            'subject_id': self.subject_id,
            'faculty_id': self.faculty_id,
            'day_of_week': self.day_of_week,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'room': self.room,
            'is_active': self.is_active,
        }

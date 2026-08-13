"""Subject Models"""


class Subject:
    """Subject taught at the college."""

    def __init__(self, id=None, name=None, code=None, department=None,
                 semester=1, credits=0, is_active=True):
        self.id = id
        self.name = name
        self.code = code
        self.department = department
        self.semester = semester
        self.credits = credits
        self.is_active = is_active

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'department': self.department,
            'semester': self.semester,
            'credits': self.credits,
            'is_active': self.is_active,
        }


class FacultySubject:
    """Assignment of a subject to a faculty member."""

    def __init__(self, id=None, faculty_id=None, subject_id=None, class_id=None, is_active=True):
        self.id = id
        self.faculty_id = faculty_id
        self.subject_id = subject_id
        self.class_id = class_id
        self.is_active = is_active

    def to_dict(self):
        return {
            'id': self.id,
            'faculty_id': self.faculty_id,
            'subject_id': self.subject_id,
            'class_id': self.class_id,
            'is_active': self.is_active,
        }

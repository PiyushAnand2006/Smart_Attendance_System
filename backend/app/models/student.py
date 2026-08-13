"""Student & Parent Models"""


class Student:
    """Student with a permanent identity (STU####)."""

    def __init__(self, id=None, student_id=None, first_name=None, last_name=None,
                 roll_number=None, class_id=None, section=None, department=None,
                 enrollment_status='incomplete', is_active=True):
        self.id = id
        self.student_id = student_id
        self.first_name = first_name
        self.last_name = last_name
        self.roll_number = roll_number
        self.class_id = class_id
        self.section = section
        self.department = department
        self.enrollment_status = enrollment_status
        self.is_active = is_active

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': f"{self.first_name or ''} {self.last_name or ''}".strip(),
            'roll_number': self.roll_number,
            'class_id': self.class_id,
            'section': self.section,
            'department': self.department,
            'enrollment_status': self.enrollment_status,
            'is_active': self.is_active,
        }


class ParentGuardian:
    """Parent or guardian linked to a student."""

    def __init__(self, id=None, student_id=None, name=None,
                 whatsapp_number=None, relationship='father'):
        self.id = id
        self.student_id = student_id
        self.name = name
        self.whatsapp_number = whatsapp_number
        self.relationship = relationship

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'name': self.name,
            'whatsapp_number': self.whatsapp_number,
            'relationship': self.relationship,
        }

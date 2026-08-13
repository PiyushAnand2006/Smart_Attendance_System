"""Faculty Model"""


class Faculty:
    """Faculty member."""

    def __init__(self, id=None, faculty_id=None, user_id=None, first_name=None,
                 last_name=None, department=None, is_active=True):
        self.id = id
        self.faculty_id = faculty_id
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.department = department
        self.is_active = is_active

    def to_dict(self):
        return {
            'id': self.id,
            'faculty_id': self.faculty_id,
            'user_id': self.user_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': f"{self.first_name or ''} {self.last_name or ''}".strip(),
            'department': self.department,
            'is_active': self.is_active,
        }

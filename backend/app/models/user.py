"""User Model"""


class User:
    """Application user (admin / faculty / student)."""

    def __init__(self, id=None, user_id=None, email=None, first_name=None,
                 last_name=None, role='student', is_active=True):
        self.id = id
        self.user_id = user_id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.role = role
        self.is_active = is_active

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'role': self.role,
            'is_active': self.is_active,
        }

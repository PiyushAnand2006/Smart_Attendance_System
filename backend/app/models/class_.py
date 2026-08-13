"""Class & Section Models"""


class ClassModel:
    """Academic class (e.g. Computer Science)."""

    def __init__(self, id=None, name=None, code=None, department=None,
                 batch_year=None, is_active=True):
        self.id = id
        self.name = name
        self.code = code
        self.department = department
        self.batch_year = batch_year
        self.is_active = is_active

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'department': self.department,
            'batch_year': self.batch_year,
            'is_active': self.is_active,
        }


class Section:
    """Section within a class (e.g. CSE-A)."""

    def __init__(self, id=None, class_id=None, name=None, is_active=True):
        self.id = id
        self.class_id = class_id
        self.name = name
        self.is_active = is_active

    def to_dict(self):
        return {
            'id': self.id,
            'class_id': self.class_id,
            'name': self.name,
            'is_active': self.is_active,
        }

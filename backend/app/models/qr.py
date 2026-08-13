"""QR Code Models"""


class QRIdentity:
    """Permanent QR identity assigned to a student."""

    def __init__(self, id=None, student_id=None, qr_identifier=None, is_active=True):
        self.id = id
        self.student_id = student_id
        self.qr_identifier = qr_identifier
        self.is_active = is_active

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'qr_identifier': self.qr_identifier,
            'is_active': self.is_active,
        }


class QRToken:
    """Ephemeral token generated for a live QR attendance session."""

    def __init__(self, id=None, session_id=None, token=None,
                 expires_at=None, is_active=True):
        self.id = id
        self.session_id = session_id
        self.token = token
        self.expires_at = expires_at
        self.is_active = is_active

    def to_dict(self):
        return {
            'id': self.id,
            'session_id': self.session_id,
            'token': self.token,
            'expires_at': self.expires_at,
            'is_active': self.is_active,
        }

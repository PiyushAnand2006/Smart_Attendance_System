"""Notification Queue and Log Models"""


class NotificationTemplate:
    """Reusable WhatsApp message template."""

    def __init__(self, id=None, name=None, display_name=None, content=None,
                 variables='', is_active=True):
        self.id = id
        self.name = name
        self.display_name = display_name
        self.content = content
        self.variables = variables
        self.is_active = is_active

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'display_name': self.display_name,
            'content': self.content,
            'variables': self.variables,
            'is_active': self.is_active,
        }


class NotificationQueue:
    """Notification queued for async processing."""

    def __init__(self, id=None, session_id=None, recipient_number=None,
                 message=None, status='PENDING', created_at=None):
        self.id = id
        self.session_id = session_id
        self.recipient_number = recipient_number
        self.message = message
        self.status = status
        self.created_at = created_at

    def to_dict(self):
        return {
            'id': self.id,
            'session_id': self.session_id,
            'recipient_number': self.recipient_number,
            'message': self.message,
            'status': self.status,
            'created_at': self.created_at,
        }


class NotificationLog:
    """Delivery log entry."""

    def __init__(self, id=None, queue_id=None, recipient_number=None,
                 status='PENDING', error=None, sent_at=None):
        self.id = id
        self.queue_id = queue_id
        self.recipient_number = recipient_number
        self.status = status
        self.error = error
        self.sent_at = sent_at

    def to_dict(self):
        return {
            'id': self.id,
            'queue_id': self.queue_id,
            'recipient_number': self.recipient_number,
            'status': self.status,
            'error': self.error,
            'sent_at': self.sent_at,
        }

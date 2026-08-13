"""Face Recognition Models"""


class FaceEmbedding:
    """Stored face embedding for a student."""

    def __init__(self, id=None, student_id=None, embedding=None,
                 samples=0, is_active=True):
        self.id = id
        self.student_id = student_id
        self.embedding = embedding
        self.samples = samples
        self.is_active = is_active

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'samples': self.samples,
            'is_active': self.is_active,
        }

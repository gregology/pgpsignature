import re
from app import db
from sqlalchemy import func
from sqlalchemy.orm import validates


class Signature(db.Model):
    __tablename__ = 'signatures'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())

    A_UPPERCASE   = ord('A')
    ALPHABET_SIZE = 26
    PGP_SIGNATURE_REGEX = '^-----BEGIN PGP SIGNED MESSAGE-----(.*\n)*-----BEGIN PGP SIGNATURE-----(.*\n)*-----END PGP SIGNATURE-----$'

    @validates('content')
    def validate_content(self, key, content):
        assert bool(re.search(self.PGP_SIGNATURE_REGEX, content)), \
            'content must be valid PGP signature'
        return content

    def __init__(self, content):
        self.content = content.strip()

    def __repr__(self):
        return f'<Signature {self.key()}>'

    def _decompose(self, number):
        while number:
            number, remainder = divmod(number - 1, self.ALPHABET_SIZE)
            yield remainder

    def _base_10_to_alphabet(self, number):
        return ''.join(
                chr(self.A_UPPERCASE + part)
                for part in self._decompose(number)
        )[::-1]

    def key(self):
        return self._base_10_to_alphabet(self.id)

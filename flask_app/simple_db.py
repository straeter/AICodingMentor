import re
import secrets
import string
from datetime import datetime

from sqlalchemy.inspection import inspect

from flask_app.app import db


class Challenge(db.Model):
    __tablename__ = 'challenge'

    challengeId = db.Column(db.String(16), primary_key=True)
    p_language = db.Column(db.String(100), nullable=False)
    language = db.Column(db.String(100), nullable=False)
    difficulty = db.Column(db.Integer, nullable=False)
    length = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, default="")

    title = db.Column(db.String(100), nullable=False)
    assignment = db.Column(db.Text, nullable=False)
    code = db.Column(db.Text, default="")
    solution = db.Column(db.Text, nullable=False)
    hint = db.Column(db.Text, nullable=False)
    attempt = db.Column(db.Text, default="")
    feedback = db.Column(db.Text, default="")
    status = db.Column(db.String(10), default="open")
    updated_at = db.Column(db.DateTime, default=datetime.now)

    def update(self, data):
        for attr, value in data.items():
            setattr(self, attr, value)

    def to_dict(self):
        result = {
            c.key: str(getattr(self, c.key)) if isinstance(getattr(self, c.key), datetime) else getattr(self, c.key)
            for c in inspect(self).mapper.column_attrs}
        return result

    def __repr__(self):
        return f"Challenge('{self.title}', '{self.updated_at}')"


def generate_unique_id(length=16):
    characters = string.ascii_letters  # Uppercase and lowercase letters
    return ''.join(secrets.choice(characters) for _ in range(length))


def split_response(message: str) -> dict:
    """ Split the streaming response message from challenge query into different parts
    :param message:
    :return: dict with keys: assignment, code, solution, hint
    """

    allowed_keys = ['ASSIGNMENT', 'CODE', 'SOLUTION', 'HINT', 'TITLE', 'END']
    pattern = r'§(' + '|'.join(allowed_keys) + r')§\s*([\s\S]*?)(?=§(?:' + '|'.join(allowed_keys) + r')§|§)'
    result_dict = {key.lower(): value.strip() for key, value in re.findall(pattern, message)}

    return result_dict


def db_save_challenge(challengeId, response, params):
    challenge_dict = split_response("§ASSIGNMENT§" + response + "§END§")
    challenge = Challenge(challengeId=challengeId, **params, **challenge_dict)
    db.session.add(challenge)
    db.session.commit()

    return challenge


def db_get_challenge(challengeId):
    challenge = Challenge.query.filter_by(challengeId=challengeId).first()
    return challenge


def db_delete_challenge(challengeId):
    challenge = Challenge.query.filter_by(challengeId=challengeId).first()
    if challenge:
        db.session.delete(challenge)
        db.session.commit()
        return True
    return False


def db_update_challenge(challengeId, **kwargs):
    challenge = Challenge.query.filter_by(challengeId=challengeId).first()
    if challenge:
        challenge.update(kwargs)
        challenge.updated_at = datetime.now()
        db.session.commit()
        return True
    return False


def db_get_all_challenges():
    challenges = Challenge.query.order_by(Challenge.updated_at.desc()).all()
    return challenges


def get_similar_challenges(
        p_language: str, language: str, difficulty: str, length: str, description: str, **params
):
    query = Challenge.query.filter_by(
        p_language=p_language,
        language=language,
        difficulty=difficulty,
        length=length,
        description=description
    ).order_by(Challenge.updated_at.desc()).limit(20)

    similar_challenges = query.all()

    return similar_challenges

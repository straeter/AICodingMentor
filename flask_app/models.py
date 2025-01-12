import secrets
import string
from _datetime import datetime, timezone

from sqlalchemy.inspection import inspect

from flask_app.app import db


def generate_unique_id(length=16):
    characters = string.ascii_letters  # Uppercase and lowercase letters
    return ''.join(secrets.choice(characters) for _ in range(length))


class Updateable:
    def update(self, data):
        for attr, value in data.items():
            setattr(self, attr, value)

    def to_dict(self, include: list[str] = None, deep_include: list[str] = None, history: bool = False):
        result = {
            c.key: str(getattr(self, c.key)) if isinstance(getattr(self, c.key), datetime) else getattr(self, c.key)
            for c in inspect(self).mapper.column_attrs}

        # if history is False, remove all attributes ending with 'History'
        if not history:
            result = {k: v for k, v in result.items() if not k.endswith('History')}

        if include:
            for rel_name in include:
                # Get the relationship attribute
                rel_obj = getattr(self, rel_name, None)

                # If the relationship object is a single instance (one-to-one or many-to-one)
                if rel_obj is not None:
                    if isinstance(rel_obj, list):  # many-to-many or one-to-many
                        result[rel_name] = [item.to_dict(include=deep_include) for item in rel_obj]
                    else:  # one-to-one or many-to-one
                        if str(type(rel_obj)) == "<class 'sqlalchemy.orm.dynamic.AppenderQuery'>":
                            rel_obj_new = rel_obj.first()
                            if rel_obj_new:
                                result[rel_name] = rel_obj_new.to_dict(include=deep_include)
                            else:
                                result[rel_name] = None
                        else:
                            result[rel_name] = rel_obj.to_dict(include=deep_include)
        return result


class Scan(db.Model, Updateable):
    __tablename__ = 'scans'

    id = db.Column(db.Integer, primary_key=True)
    scanId = db.Column(db.String, unique=True, default=generate_unique_id)
    created_at = db.Column(db.DateTime(), default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(), default=None)

    scan_type = db.Column(db.String, nullable=False)
    repo = db.Column(db.String)
    branch = db.Column(db.String)
    base_path = db.Column(db.String)
    title = db.Column(db.String, nullable=False)
    file_types = db.Column(db.JSON, default=[])
    files = db.Column(db.JSON, default=[])
    scanned_files = db.Column(db.JSON, default=[])
    progress = db.Column(db.Integer, default=0)
    status = db.Column(db.String, default="running")

    # References
    issues = db.relationship(
        'Issue',
        backref=db.backref('scan', lazy='joined'),
        lazy="joined",
        order_by='desc(Issue.level)',
        cascade="all, delete-orphan"
    )


class Issue(db.Model, Updateable):
    __tablename__ = 'issues'

    id = db.Column(db.Integer, primary_key=True)
    issueId = db.Column(db.String, unique=True, default=generate_unique_id)
    created_at = db.Column(db.DateTime(), default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(), default=None)
    filepath = db.Column(db.String, nullable=False)

    title = db.Column(db.String, nullable=False)
    reference = db.Column(db.String)
    reference_code = db.Column(db.JSON, default=[])
    level = db.Column(db.Integer, nullable=False)
    reason = db.Column(db.String, default=False)
    suggestion = db.Column(db.String, default=False)

    # References
    scan_id = db.Column(db.Integer, db.ForeignKey('scans.id'), nullable=False)

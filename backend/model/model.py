import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.attributes import QueryableAttribute
from backend.persistence.db import db


class BaseModel(db.Model):
    __abstract__ = True

    def to_dict(self):
        """Return a dictionary representation of this model."""
        return {column.key: getattr(self, attr) for attr, column in self.__mapper__.c.items()}

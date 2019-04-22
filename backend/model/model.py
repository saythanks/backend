import json
from sqlalchemy.dialects.postgresql import UUID
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

from sqlalchemy.orm.attributes import QueryableAttribute
from sqlalchemy.ext.declarative import declarative_base
from backend.persistence.db import db


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))

    time_created = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    time_updated = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        server_onupdate=db.func.now(),
        nullable=False,
    )

    privateFields = None

    def to_dict(self):
        """Return a dictionary representation of this model."""
        res = {
            column.key: getattr(self, attr)
            for attr, column in self.__mapper__.c.items()
        }

        if self.privateFields is not None:
            for field in self.privateFields:
                if field in res:
                    del res[field]

        return res


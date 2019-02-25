from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func, text

from backend.model.model import BaseModel
from backend.persistence.db import db


class Account(BaseModel):
    balance = db.Column(db.Integer)

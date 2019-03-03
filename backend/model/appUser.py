import random
import string
from enum import Enum

from sqlalchemy.dialects.postgresql import UUID
from backend.util.marshmallow import ma

from backend.model.model import BaseModel
from backend.persistence.db import db


class Role(Enum):
    user = 0
    admin = 1


class AppUser(BaseModel):
    __tablename__ = "app_user"

    user_id = db.Column(UUID, db.ForeignKey("user.id"), primary_key=True)
    user = db.relationship("User", backref="user_apps")

    app_id = db.Column(UUID, db.ForeignKey("app.id"), primary_key=True)
    app = db.relationship("App", backref="app_users")

    role = db.Column(db.Enum(Role), nullable=False, server_default="admin")

    # def __init__(self, app=None, user=None):
    #     self.app = app
    #     self.user = user

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func, text

from backend.persistence.db import db
from backend.model.model import BaseModel


class Payable(BaseModel):

    app_id = db.Column(UUID, db.ForeignKey("app.id"))
    app = db.relationship("App")

    display_name = db.Column(db.Text, nullable=False)
    display_price = db.Column(db.Integer, nullable=False)

    permalink = db.Column(db.Text, nullable=True)

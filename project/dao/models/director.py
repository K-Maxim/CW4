from project.dao.models.base import BaseMixin
from project.setup_db import db
from sqlalchemy import Column, String, Integer


class Director(BaseMixin, db.Model):
    __tablename__ = "director"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"<Director '{self.name.title()}'>"

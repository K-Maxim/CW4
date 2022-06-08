from project.dao.models.base import BaseMixin
from project.setup_db import db
from sqlalchemy import Column, String, Integer


class User(BaseMixin, db.Model):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(300))
    name = Column(String(50))
    surname = Column(String(100))
    favorite_genre = Column(String(100))

    def __repr__(self):
        return f"<Movie '{self.name.title()}'>"

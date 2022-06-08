from project.dao.models.base import BaseMixin
from project.setup_db import db
from sqlalchemy import Column, String, Integer, Float, ForeignKey


class Movie(BaseMixin, db.Model):
    __tablename__ = "movie"

    id = Column(Integer, primary_key=True)
    title = Column(String(100), unique=True, nullable=False)
    description = Column(String(300))
    trailer = Column(String(300))
    year = Column(Integer)
    rating = Column(Float)
    genre_id = Column(Integer, ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    director_id = Column(Integer, ForeignKey("director.id"))
    director = db.relationship("Director")


    def __repr__(self):
        return f"<Movie '{self.name.title()}'>"

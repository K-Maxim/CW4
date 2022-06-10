from marshmallow import fields, Schema

from project.schemas.director import DirectorSchema
from project.schemas.genre import GenreSchema


class MovieSchema(Schema):
    id = fields.Int(required=True)
    title = fields.Str(required=True)
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Int()
    genre = fields.Nested(GenreSchema)
    director = fields.Nested(DirectorSchema)


from project.config import DevelopmentConfig
from project.dao.models import Genre
from project.dao.models.director import Director
from project.dao.models.movie import Movie
from project.dao.models.user import User
from project.server import create_app, db

app = create_app(DevelopmentConfig)


@app.shell_context_processor
def shell():
    return {
        "db": db,
        "Genre": Genre,
        "User": User,
        "Director": Director,
        "Movie": Movie,
    }


if __name__ == '__main__':
    app.run(port='25000')

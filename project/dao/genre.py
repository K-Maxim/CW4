from sqlalchemy.orm.scoping import scoped_session

from project.dao.models.genre import Genre


class GenreDAO:
    def __init__(self, session: scoped_session):
        self._db_session = session

    def get_by_id(self, pk):
        """
        Получаем жанр по его id, если такого id нет, то ничего не выведет
        """
        return self._db_session.query(Genre).filter(Genre.id == pk).one_or_none()

    def get_all(self):
        """
        Получаем все жанры
        """
        return self._db_session.query(Genre).all()

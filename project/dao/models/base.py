from sqlalchemy import Column, Integer


class BaseMixin(object):
    id = Column(Integer, primary_key=True, autoincrement=True)

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('%s' % os.environ.get('DATABASE_URL', 'sqlite://'), convert_unicode=True)
db_session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
)

Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    import fastmonkeys.models
    Base.metadata.create_all(bind=engine)
    # it's a hack to stop the warning about unused import
    # I have to import this way to create the database 8(
    dir(fastmonkeys.models)

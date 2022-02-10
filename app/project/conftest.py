import pytest
from project import app, db
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.scoping import scoped_session
from users.factories import UserFactory


@pytest.fixture
def api_client():
    yield app.test_client()


@pytest.fixture(scope='module')
def connection():
    connection = db.engine.connect()
    yield connection
    connection.close()


@pytest.fixture(autouse=True)
def session(connection):
    transaction = connection.begin()
    session = scoped_session(sessionmaker(bind=connection))

    session_backup = db.session
    db.session = session
    UserFactory._meta.sqlalchemy_session = db.session
    yield

    db.session = session_backup
    session.close()
    transaction.rollback()

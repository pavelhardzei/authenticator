import jwt
import pytest
from applications.factories import ApplicationFactory
from project import app, db
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.scoping import scoped_session
from users.factories import UserFactory


@pytest.fixture
def api_client():
    yield app.test_client()


@pytest.fixture
def token_user1(user1):
    return jwt.encode({'id': user1.id}, app.config['SECRET_KEY'], algorithm='HS256')


@pytest.fixture
def token_user2(user2):
    return jwt.encode({'id': user2.id}, app.config['SECRET_KEY'], algorithm='HS256')


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
    ApplicationFactory._meta.sqlalchemy_session = db.session

    for table in reversed(db.metadata.sorted_tables):
        db.session.execute(table.delete())
    db.session.commit()

    yield

    db.session = session_backup
    session.close()
    transaction.rollback()

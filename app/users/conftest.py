from project.conftest import api_client, connection, session
from pytest_factoryboy import register
from users.factories import UserFactory

register(UserFactory, 'user1', email='user1@gmail.com')
register(UserFactory, 'user2')

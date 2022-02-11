from project.conftest import api_client, connection, session, token_user1, token_user2
from pytest_factoryboy import register
from users.factories import UserFactory

register(UserFactory, 'user1', email='user1@gmail.com', username='user1')
register(UserFactory, 'user2')

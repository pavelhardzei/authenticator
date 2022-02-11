from project.conftest import api_client, connection, session, token_user1, token_user2
from pytest_factoryboy import LazyFixture, register
from applications.factories import ApplicationFactory
from users.factories import UserFactory

register(UserFactory, 'user1')
register(UserFactory, 'user2')

register(ApplicationFactory, 'app1_user1', name='app1', user_profile=LazyFixture('user1'))
register(ApplicationFactory, 'app2_user1', name='app2', user_profile=LazyFixture('user1'))

register(ApplicationFactory, 'app1_user2', user_profile=LazyFixture('user2'))

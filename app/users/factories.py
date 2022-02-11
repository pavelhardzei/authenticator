import factory
from faker import Faker
from users.models import UserProfile
from werkzeug.security import generate_password_hash

fake = Faker()


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = UserProfile

    id = factory.Sequence(lambda pk: pk)
    email = factory.Sequence(lambda _: fake.email())
    username = fake.user_name()
    password = generate_password_hash('testing321', method='sha256')

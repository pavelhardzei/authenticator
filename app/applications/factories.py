import factory
import pyotp
from applications.models import Application
from faker import Faker
from users.factories import UserFactory

fake = Faker()


class ApplicationFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Application

    id = factory.Sequence(lambda pk: pk)
    name = fake.word()
    secret = pyotp.random_base32()
    user_profile = factory.SubFactory(UserFactory)

from project import ma
from users.models import UserProfile


class UserProfileSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserProfile
        fields = ('id', 'email', 'username', 'password')
        load_only = ('password', )
        load_instance = True

from marshmallow import ValidationError, post_load
from project import ma
from users.models import UserProfile


class UserProfileSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserProfile
        fields = ('id', 'email', 'username', 'password')
        load_only = ('password', )
        load_instance = True


class UserSigninSchema(ma.Schema):
    email = ma.Email()
    password = ma.String()

    @post_load
    def check_password(self, data, *args, **kwargs):
        user = UserProfile.query.filter_by(email=data['email']).first()
        if user is None:
            raise ValidationError({'message': 'User not found'})

        if not user.check_password(data['password']):
            raise ValidationError({'message': 'Password is incorrect'})

        return user


class UserTokenSchema(ma.Schema):
    user = ma.Nested(UserProfileSchema)
    token = ma.String()

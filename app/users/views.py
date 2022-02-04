from datetime import datetime, timedelta

import jwt
from flask import Blueprint, request
from flask_restful import Api, Resource
from project import app as root
from users.models import UserProfile
from users.schemas import UserProfileSchema, UserSigninSchema, UserTokenSchema

app = Blueprint('users', __name__)
api = Api(app)


class UserSignup(Resource):
    schema = UserProfileSchema()

    def post(self):
        user = self.schema.load(request.get_json())
        user.set_password(request.get_json()['password'])

        user.save()

        return self.schema.dump(user)


class UserSignin(Resource):
    schema = UserSigninSchema()

    def post(self):
        user = self.schema.load(request.get_json())
        token = jwt.encode({'id': user.id, 'exp': datetime.utcnow() + timedelta(seconds=10)},
                           root.config['SECRET_KEY'], algorithm='HS256')

        return UserTokenSchema().dump({'user': user, 'token': token})


api.add_resource(UserSignup, '/signup/')
api.add_resource(UserSignin, '/signin/')

from datetime import datetime, timedelta

import jwt
from flask import Blueprint, request
from flask_restful import Api, Resource
from project import app as root
from project.utils import token_required
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
        token = jwt.encode({'id': user.id, 'exp': datetime.utcnow() + timedelta(minutes=30)},
                           root.config['SECRET_KEY'], algorithm='HS256')

        return UserTokenSchema().dump({'user': user, 'token': token})


class UserDetail(Resource):
    schema = UserProfileSchema()

    @token_required
    def get(self, *args, **kwargs):
        return self.schema.dump(kwargs['user'])

    @token_required
    def put(self, *args, **kwargs):
        schema = UserProfileSchema(exclude=('password', ))

        user = schema.load(request.get_json(), instance=kwargs['user'])
        user.save()

        return self.schema.dump(user)

    @token_required
    def patch(self, *args, **kwargs):
        schema = UserProfileSchema(exclude=('password', ), partial=True)

        user = schema.load(request.get_json(), instance=kwargs['user'])
        user.save()

        return self.schema.dump(user)

    @token_required
    def delete(self, *args, **kwargs):
        user = kwargs['user']
        user.delete()

        return {'message': 'No content'}, 204


api.add_resource(UserDetail, '/')
api.add_resource(UserSignup, '/signup/')
api.add_resource(UserSignin, '/signin/')

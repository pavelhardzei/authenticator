from flask import Blueprint, request
from flask_restful import Api, Resource
from project import db
from users.models import UserProfile
from users.schemas import UserProfileSchema
from werkzeug.security import check_password_hash, generate_password_hash

app = Blueprint('users', __name__)
api = Api(app)


class UserSignup(Resource):
    schema = UserProfileSchema()

    def post(self):
        user = self.schema.load(request.get_json())
        user.password = generate_password_hash(user.password, method='sha256')

        db.session.add(user)
        db.session.commit()

        return self.schema.dump(user)


api.add_resource(UserSignup, '/signup/')

from functools import wraps
from http import HTTPStatus

import jwt
from flask import request
from project import app
from users.models import UserProfile


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return {'message': 'Token is required'}, HTTPStatus.UNAUTHORIZED
        if len(token.split(' ')) != 2 or token.split(' ')[0] != 'Token':
            return {'message': 'Required format: Token <your_token>'}, HTTPStatus.BAD_REQUEST

        token = token.split(' ')[1]
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])

        user = UserProfile.query.filter_by(id=data['id']).first()
        if user is None:
            return {'message': 'User not found'}, HTTPStatus.UNAUTHORIZED

        kwargs['user'] = user

        return f(*args, **kwargs)

    return decorator

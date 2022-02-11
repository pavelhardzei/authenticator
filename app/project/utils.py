from functools import wraps

import jwt
from flask import request
from project import app
from users.models import UserProfile


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return {'message': 'Token is required'}, 400
        if len(token.split(' ')) != 2 or token.split(' ')[0] != 'Token':
            return {'message': 'Required format: Token <your_token>'}, 400

        try:
            token = token.split(' ')[1]
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            user = UserProfile.query.filter_by(id=data['id']).first()

            kwargs['user'] = user
        except Exception as e:
            return {'message': f'{e}'}, 400

        return f(*args, **kwargs)

    return decorator

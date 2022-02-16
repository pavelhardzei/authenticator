from http import HTTPStatus


def handle_error(e):
    return {'message': e.args}, HTTPStatus.BAD_REQUEST

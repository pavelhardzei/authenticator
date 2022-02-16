from http import HTTPStatus


def handle_error(e):
    return {'message': e.args}, HTTPStatus.INTERNAL_SERVER_ERROR

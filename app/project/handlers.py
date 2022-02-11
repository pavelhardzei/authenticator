def handle_error(e):
    return {'message': e.args}, 400

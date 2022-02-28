from http import HTTPStatus

from werkzeug.exceptions import HTTPException


class LogicError(HTTPException):
    code = HTTPStatus.INTERNAL_SERVER_ERROR
    description = 'Server error'

    def __init__(self, code=None, description=None):
        self.code = code or self.code
        self.description = description or self.description

        self.response = {'message': self.description}, self.code

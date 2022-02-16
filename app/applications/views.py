import pyotp
from applications.models import Application
from applications.schemas import ApplicationSchema, TotpSchema
from flask import Blueprint, request
from flask_restful import Api, Resource
from project.exceptions import LogicError
from project.utils import token_required

app = Blueprint('applications', __name__)
api = Api(app)


class ApplicationList(Resource):
    schema = ApplicationSchema()

    @token_required
    def get(self, *args, **kwargs):
        user = kwargs['user']

        return self.schema.dump(user.applications, many=True)

    @token_required
    def post(self, *args, **kwargs):
        user = kwargs['user']

        application = self.schema.load(request.get_json())
        application.user_id = user.id
        application.save()

        return self.schema.dump(application), 201


class ApplicationDetail(Resource):
    schema = ApplicationSchema()

    @token_required
    def get(self, *args, **kwargs):
        return self.schema.dump(self.get_object(*args, **kwargs))

    @token_required
    def delete(self, *args, **kwargs):
        application = self.get_object(*args, **kwargs)
        application.delete()

        return {}, 204

    @token_required
    def put(self, *args, **kwargs):
        schema = ApplicationSchema(exclude=('secret', ))

        instance = self.get_object(*args, **kwargs)
        application = schema.load(request.get_json(), instance=instance)
        application.save()

        return self.schema.dump(application)

    def get_object(self, *args, **kwargs):
        user = kwargs['user']
        application = Application.query.filter_by(id=kwargs['id']).first()

        self.check_permissions(user, application)

        return application

    def check_permissions(self, user, obj):
        if obj is None:
            raise LogicError(404, 'Resource not found')
        if obj.user_id != user.id:
            raise LogicError(403, 'Forbidden')


class ApplicationCode(Resource):
    schema = TotpSchema()

    @token_required
    def get(self, *args, **kwargs):
        user = kwargs['user']
        application = Application.query.filter_by(id=kwargs['id']).first()

        if application is None:
            raise LogicError(404, 'Resource not found')
        if application.user_id != user.id:
            raise LogicError(403, 'Forbidden')

        totp = pyotp.TOTP(application.secret)

        return self.schema.dump({'totp': totp.now()})


api.add_resource(ApplicationList, '/')
api.add_resource(ApplicationDetail, '/<int:id>/')
api.add_resource(ApplicationCode, '/<int:id>/code/')

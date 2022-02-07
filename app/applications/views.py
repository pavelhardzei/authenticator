from applications.models import Application
from applications.schemas import ApplicationSchema
from flask import Blueprint, request
from flask_restful import Api, Resource
from project.utils import token_required

app = Blueprint('applications', __name__)
api = Api(app)


class ApplicationList(Resource):
    schema = ApplicationSchema()

    @token_required
    def get(self, *args, **kwargs):
        user = kwargs['user']
        applcations = Application.query.filter_by(user_id=user.id).all()

        return self.schema.dump(applcations, many=True)

    @token_required
    def post(self, *args, **kwargs):
        user = kwargs['user']

        application = self.schema.load(request.get_json())
        application.user_id = user.id
        application.save()

        return self.schema.dump(application)


api.add_resource(ApplicationList, '/')

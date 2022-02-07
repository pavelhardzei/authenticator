from applications.models import Application
from flask import Blueprint
from flask_restful import Api, Resource

app = Blueprint('applications', __name__)
api = Api(app)

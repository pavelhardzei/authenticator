from applications.models import Application
from project import ma


class ApplicationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Application
        fields = ('id', 'name', 'secret')
        load_only = ('secret', )
        load_instance = True

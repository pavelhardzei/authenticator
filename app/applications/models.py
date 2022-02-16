from project import db
from project.mixins import DbMixin


class Application(db.Model, DbMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    secret = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'), nullable=False)

    def __repr__(self):
        return f'Application({self.name})'

from project import db
from project.mixins import DbMixin
from werkzeug.security import check_password_hash, generate_password_hash


class UserProfile(db.Model, DbMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    applications = db.relationship('Application', cascade='all, delete', lazy=True,
                                   backref=db.backref('user_profile', lazy=True))

    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'User({self.email})'

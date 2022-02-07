from applications.views import app as applications_app
from flask import Flask
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from project.config import Config
from users.views import app as users_app

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db, compare_type=True)


app.register_blueprint(users_app, url_prefix='/user')
app.register_blueprint(applications_app, url_prefix='/applications')

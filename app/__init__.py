import os
import config
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from app.commands import sample_data


app = Flask(__name__)
app.config.from_object(config.Config)
app.config.from_envvar('WOLFIT_SETTINGS')
app.config['SQLALCHEMY_DATABASE_URI'] = config.Config.DATABASE_URI(app)
app.register_blueprint(sample_data)

db = SQLAlchemy(app)
login = LoginManager(app)
migrate = Migrate(app, db)
bootstrap = Bootstrap(app)
microservice_url = os.getenv("ACTIVITY_LOG_URL", "http://localhost:5000/api/activities")

from app import models, routes

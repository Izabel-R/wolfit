import os
from flask import Flask
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'izabelsecretk3y318xyzCS465hw2')
app.config['MICROSERVICE_BASE_URL'] = os.getenv('MICROSERVICE_BASE_URL', 'http://localhost:5000')

db = SQLAlchemy()
login_manager = LoginManager(app)
bootstrap = Bootstrap(app)
microservice_url = os.getenv("ACTIVITY_LOG_URL", "http://localhost:5000/api/activities")

from app import routes
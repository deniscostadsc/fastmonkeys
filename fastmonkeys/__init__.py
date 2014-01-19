import os

from flask import Flask
from flask_login import LoginManager

from fastmonkeys.models import Monkey

app = Flask(__name__)

app.secret_key = os.environ.get('SECRET_KEY')

from fastmonkeys.views import *

login_manager = LoginManager()

login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return Monkey.query.get(user_id)

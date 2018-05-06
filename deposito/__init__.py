from cryptacular.bcrypt import BCRYPTPasswordManager
from flask import Flask
from flask_login import LoginManager
from deposito.models import *
app = Flask(__name__)

app.config.from_envvar('DEPOSITO_SETTINGS')

# flask-login
login_manager = LoginManager()
login_manager.setup_app(app)
login_manager.login_view = 'login'

# cryptacular password manager
pw_manager = BCRYPTPasswordManager()

# flask-sqlalchemy
db.init_app(app)

import deposito.views

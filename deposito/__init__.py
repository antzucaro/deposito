from flask import Flask
from flask_openid import OpenID
from deposito.models import *
app = Flask(__name__)
app.config.from_envvar('DEPOSITO_SETTINGS')
oid = OpenID(app, 'oidstore')
db.init_app(app)

import deposito.views

from flask import Flask
from .main.routes import main
from .api.routes import api
from .auth.routes import auth
from config import Config

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from .models import db as root_db
from .models import login, marsh

from flask_marshmallow import Marshmallow

from flask_cors import CORS

#grab jsonencoder from helpers
from marvel.help import JSONEncoder

app = Flask(__name__)

app.register_blueprint(main)
app.register_blueprint(api)
app.register_blueprint(auth)

app.config.from_object(Config)


root_db.init_app(app)

migrate = Migrate(app, root_db)
login.init_app(app)
login.login_view = 'auth.signin'

marsh.init_app(app)

app.json_encoder = JSONEncoder



CORS(app)
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt  # Module for hashing the passwords

app = Flask(__name__)
app.config['SECRET_KEY'] = '0bf73b1b8885221e9660f2e18dffa647'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://vijaydb:vijay@localhost/\
vijaydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # function name of login route
login_manager.login_message_category = 'warning'  # bootstrap class


from quora import routes, models, errors  # noqa: E402, F401

migrate = Migrate()
migrate.init_app(app, db)

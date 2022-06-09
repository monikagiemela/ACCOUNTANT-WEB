#import psycopg2
from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

from app.UTILS.helpers import usd, absolute
from flask_migrate import Migrate


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filters
app.jinja_env.filters["usd"] = usd
app.jinja_env.filters["absolute"] = absolute

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Create a database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///accountant.db'
#DATABASE_URL = os.environ['DATABASE_URL']
#app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL.replace("postgres", "postgresql")

db = SQLAlchemy(app)
migrate = Migrate(app, db)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

from app import models

from app.views.views_index import index
from app.views.views_history import history 
from app.views.views_login import login
from app.views.views_logout import logout
from app.views.views_register import register
from app.views.views_buy import buy
from app.views.views_sell import sell
from app.views.views_user import user
from os import getenv
from flask_sqlalchemy import SQLAlchemy
from app import app

db_url = getenv("DATABASE_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = db_url
db = SQLAlchemy(app)

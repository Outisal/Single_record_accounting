from app import app
from flask_sqlalchemy import SQLAlchemy
from os import getenv

db_url = getenv("DATABASE_URL")
print(db_url)
app.config["SQLALCHEMY_DATABASE_URI"] = db_url
db = SQLAlchemy(app)
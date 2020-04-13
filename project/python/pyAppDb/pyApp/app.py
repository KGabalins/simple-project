from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres//postgres:db-frknz@db:5432/example?sslmode=disable"
db = SQLAlchemy(app)

db.drop_all()
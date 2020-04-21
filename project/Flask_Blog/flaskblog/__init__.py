from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blogSite.db'
app.config['SECRET_KEY'] = 'fc1fe1d849a56333d60b3b09839d2529'
# Izveidota datubaazes instance
db = SQLAlchemy(app)

from flaskblog import routes
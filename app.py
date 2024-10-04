from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from dotenv import load_dotenv, find_dotenv
import os
from pages import pages
from models import db, Users


app = Flask(__name__)

load_dotenv(find_dotenv())
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.register_blueprint(pages)

if __name__ == "__main__":
    app.run(
        host=os.getenv("IP", "0.0.0.0"), 
        port=int(os.getenv("PORT", 8080)), 
        debug=True)
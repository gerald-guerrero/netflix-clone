from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from pages import pages
from models import db


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

app.register_blueprint(pages)

if __name__ == "__main__":
    app.run(
        host=os.getenv("IP", "0.0.0.0"), 
        port=int(os.getenv("PORT", 8080)), 
        debug=True)
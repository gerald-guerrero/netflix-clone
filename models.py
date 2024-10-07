from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    favorites = db.relationship('Favorites', backref='users', lazy='dynamic')

class Movies_Shows(db.Model):
    __tablename__ = 'movies_shows'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    genre = db.Column(db.String(100))
    description = db.Column(db.Text)
    release_date = db.Column(db.String(100))
    duration = db.Column(db.Integer)
    favorites = db.relationship('Favorites', backref='movies_shows', lazy='dynamic')
    
class Favorites(db.Model):
    __tablename__ = 'favorites'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    movies_shows_id = db.Column(db.Integer, db.ForeignKey('movies_shows.id'))
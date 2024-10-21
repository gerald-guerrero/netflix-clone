from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    favorites = db.relationship('Favorites', backref='users', lazy='dynamic')
    history = db.relationship('History', backref='users', lazy='dynamic')

    def __init__(self, username, password):
        self.username = username
        self.password = bcrypt.generate_password_hash(password=password)
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

class Movies_Shows(db.Model):
    __tablename__ = 'movies_shows'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    genre = db.Column(db.String(100))
    description = db.Column(db.Text)
    release_date = db.Column(db.String(100))
    duration = db.Column(db.Integer)
    favorites = db.relationship('Favorites', backref='movies_shows', lazy='dynamic')
    history = db.relationship('History', backref='movies_shows', lazy='dynamic')

    def __init__(self, title, genre, description, release_date, duration):
        self.title = title
        self.genre = genre
        self.description = description
        self.release_date = release_date
        self.duration = duration
    
class Favorites(db.Model):
    __tablename__ = 'favorites'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    movies_shows_id = db.Column(db.Integer, db.ForeignKey('movies_shows.id'))

    def __init__(self, user_id, movies_shows_id):
        self.user_id = user_id
        self.movies_shows_id = movies_shows_id

class History(db.Model):
    __tablename__ = 'history'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    movies_shows_id = db.Column(db.Integer, db.ForeignKey('movies_shows.id'))

    def __init__(self, user_id, movies_shows_id):
        self.user_id = user_id
        self.movies_shows_id = movies_shows_id

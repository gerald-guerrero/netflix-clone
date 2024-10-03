
from flask import Blueprint, render_template, url_for
from models import Movies_Shows

pages = Blueprint("pages", __name__)

@pages.route("/")
def index():
    links = {"Home": url_for("pages.index"), "Login": url_for("pages.login"), "Register": url_for("pages.register"), "List": url_for("pages.list"), "Details": url_for("pages.detail"), "Favorites": url_for("pages.favorites")}
    
    return render_template("index.html", links = links)

@pages.route("/login")
def login():
    return render_template("login.html")

@pages.route("/register")
def register():
    return render_template("register.html")

@pages.route("/list")
def list():
    movies_shows = Movies_Shows.query.all()
    movies_shows_list = []
    for entry in movies_shows:
        entry_dict = {'id': entry.id, 'title': entry.title, 'genre': entry.genre, 'description': entry.description, 'release_date': entry.release_date, 'duration': entry.duration}
        movies_shows_list.append(entry_dict)
    return render_template("list.html", Movies_Shows = movies_shows_list)

@pages.route("/detail")
def detail():
    return render_template("detail.html")

@pages.route("/favorites")
def favorites():
    return render_template("favorites.html")


from flask import Blueprint, render_template, url_for, redirect, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Users, Movies_Shows, Favorites

pages = Blueprint("pages", __name__)

@pages.route("/")
def index():
    """
    route for homepage and serves as main directory for app containing links for relevant pages
    can be accessed without being signed in
    """
    
    return render_template("index.html")

@pages.route("/login")
def login():
    """
    route for login page; cannot be accessed if already signed in
    """
    if "name" in session:
        return redirect(url_for("pages.index"))
    return render_template("login.html")

@pages.route("/login_input", methods=["GET", "POST"])
def login_input():
    """
    handles user input on the login page's input form
    checks if the submitted username exists and if the hashed password is correct
    manages login state by updating session["name"] with username
    """
    username_input = request.form.get("username")
    password_input = request.form.get("password")

    user_db = Users.query.filter_by(username=username_input).first()

    if user_db and check_password_hash(user_db.password, password_input):
        print("correct username and login")
        session["name"] = user_db.username
    else:
        print("incorrect username or password")
        return redirect(url_for("pages.login"))

    return redirect(url_for("pages.index"))

@pages.route("/register")
def register():
    """
    route for registration page; cannot be accessed if already signed in
    """
    if "name" in session:
        return redirect(url_for("pages.index"))
    return render_template("register.html")

@pages.route("/register_input", methods=["GET", "POST"])
def register_input():
    """
    handles user input for registration page's input form
    gets the user input and checks adds the username and hashed password if username does not already exist in the database
    """
    username_input = request.form.get("username")
    password_input = request.form.get("password")
    password_hashed = generate_password_hash(password_input)

    user_db = Users.query.filter_by(username=username_input).first()
    print(username_input, password_hashed)
    if user_db is None:
        print("User can be registered")
        user = Users(username = username_input, password = password_hashed)
        db.session.add(user)
        db.session.commit()
    else:
        print("user alerady exists")
        return redirect(url_for("pages.register"))
        
    return redirect(url_for("pages.index"))

@pages.route("/logout")
def logout():
    """
    handles logout functionality from webpage
    logs out by removing "name" attribute from session["name"]
    """
    session.pop("name", None)
    return redirect(url_for("pages.index"))

@pages.route("/list")
def list():
    """
    route for list page that displays the complete catalog of movies and shows
    only accessible when logged in by checking if session has the "name" attribute
    """
    if "name" not in session:
        return redirect(url_for("pages.login"))
     
    movies_shows = Movies_Shows.query.all()
    page_title = "Full Catalog"
    return render_template("list.html", catalog = movies_shows, page_title = page_title)

@pages.route("/detail/<int:media_id>")
def detail(media_id):
    """
    route for detail page that shows the complete information for the selected movie
    only accessible when logged in by checking if session has the "name" attribute
    """
    if "name" not in session:
        return redirect(url_for("pages.login"))
    
    entry = Movies_Shows.query.filter_by(id=media_id).first()
    movie_show = {'id': entry.id, 'title': entry.title, 'genre': entry.genre, 'description': entry.description, 'release_date': entry.release_date, 'duration': entry.duration}
    print(movie_show)
    return render_template("detail.html", movie_show = movie_show)

@pages.route("/favorites")
def favorites():
    """
    route for favorites page that shows the list of favorites for the current user
    only accessible when logged in by checking if session has the "name" attribute
    """
    if "name" not in session:
        return redirect(url_for("pages.login"))
    
    return render_template("favorites.html")

@pages.route("/title", methods=["GET"])
def title(title_input=None):
    """
    
    """
    
    if "name" not in session:
        return redirect(url_for("pages.login"))

    title_input = request.args.get("title_input")
    print(title_input)
    return redirect(url_for("pages.listFiltered", filter="title", name=title_input))

@pages.route("/list/<filter>+<name>")
def listFiltered(filter, name):
    """
    
    """
    if "name" not in session:
        return redirect(url_for("pages.login"))
    

    if (filter == "title"):
        movies_shows = Movies_Shows.query.filter(Movies_Shows.title.like(f"%{name}%"))
        page_title = "Search Results For: " + name
    elif(filter == "genre"):
        movies_shows = Movies_Shows.query.filter_by(genre = name)
        page_title = "Filtered By Genre: " + name

    print(movies_shows.count())
    return render_template("list.html", catalog=movies_shows, page_title = page_title)
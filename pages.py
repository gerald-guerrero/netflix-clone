
from flask import Blueprint, render_template, url_for, redirect, request, session, flash
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
        flash("You are now logged in")
        session["name"] = user_db.username
        session["watch_history"] = []
    else:
        flash("Incorrect credentials")
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

    if user_db is None:
        flash("User is now registered")
        user = Users(username = username_input, password = password_hashed)
        db.session.add(user)
        db.session.commit()
    else:
        flash("User already exists")
        return redirect(url_for("pages.register"))
        
    return redirect(url_for("pages.index"))

@pages.route("/logout")
def logout():
    """
    handles logout functionality from webpage
    logs out by removing "name" attribute from session["name"]
    """
    session.pop("name", None)
    session.pop("watch_history", None)
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

@pages.route("/list/<filter>+<name>")
def listFiltered(filter, name):
    """
    Finds entries from Movies_Shows model based on the provided filter type and name
    The function can query the database for entries that contain the provided name input, or
    it can filter by the given genre if the genre type filter is given
    """
    if "name" not in session:
        return redirect(url_for("pages.login"))
    

    if (filter == "title"):
        movies_shows = Movies_Shows.query.filter(Movies_Shows.title.like(f"%{name}%"))
        page_title = "Search Results For: " + name
    elif(filter == "genre"):
        movies_shows = Movies_Shows.query.filter_by(genre = name)
        page_title = "Filtered By Genre: " + name

    return render_template("list.html", catalog=movies_shows, page_title = page_title)

@pages.route("/title", methods=["GET"])
def title():
    """
    When the submit button is clicked for the page menu, the text input is retrieved, the filter
    is set to "title", and the page is redirected to listFiltered to search for the given title
    """
    
    if "name" not in session:
        return redirect(url_for("pages.login"))

    title_input = request.args.get("title_input")

    return redirect(url_for("pages.listFiltered", filter="title", name=title_input))

@pages.route("/detail/<int:movies_shows_id>")
def detail(movies_shows_id):
    """
    route for detail page that shows the complete information for the selected movie
    only accessible when logged in by checking if session has the "name" attribute
    """
    if "name" not in session:
        return redirect(url_for("pages.login"))
    
    movie_show = Movies_Shows.query.filter_by(id=movies_shows_id).first()
    user = Users.query.filter_by(username=session["name"]).first()
    if(user.favorites.filter_by(movies_shows_id=movies_shows_id).first()):
        print("Is in Favorites")
        favoriteLabel = "Remove from Favorites"
    else:
        print("Not in favorites")
        favoriteLabel = "Add to Favorites"

    if "watch_history" in session:
        session["watch_history"].insert(0, {"id": movie_show.id, "title": movie_show.title})
        print(session["watch_history"])

    return render_template("detail.html", movie_show = movie_show, favoriteLabel = favoriteLabel)

@pages.route("/favoritesUpdate/<int:movies_shows_id>")
def favoritesUpdate(movies_shows_id):
    """
    Connected to favorites button on the "/detail" page. Checks if the current movie or show is
    already in the current user's favorites with the provided movies_shows_id. The current movie 
    or show is added or removed accordingly based on this. 
    The first entry in the watch history is removed to prevent favoritesUpdate from creating a 
    duplicate entry. The entry will be added again when pages.detail is reloaded
    """
    if "name" not in session:
        return redirect(url_for("pages.login"))

    user = Users.query.filter_by(username=session["name"]).first()
    if (user.favorites.filter_by(movies_shows_id=movies_shows_id).first()):
        print("Media will be removed from favorites")
        user.favorites.filter_by(movies_shows_id=movies_shows_id).delete()
    else:
        print("media will be added to favorites")
        favEntry = Favorites(user_id=user.id, movies_shows_id = movies_shows_id)
        db.session.add(favEntry)
    
    db.session.commit()
    session["watch_history"].pop(0)

    return redirect(url_for("pages.detail", movies_shows_id = movies_shows_id))

@pages.route("/favorites")
def favorites():
    """
    route for favorites page that shows the list of favorites for the current user
    only accessible when logged in by checking if session has the "name" attribute
    """
    if "name" not in session:
        return redirect(url_for("pages.login"))
    
    user = Users.query.filter_by(username=session["name"]).first()
    favorites = user.favorites.all()
    movies_shows = []
    for entry in favorites:
        movies_shows.append(Movies_Shows.query.filter_by(id = entry.movies_shows_id).first())
    return render_template("list.html", catalog = movies_shows, page_title = "Favorites")


@pages.route("/history")
def history():
    """
    Displays a list of links from session["watch_history] based on the movies_shows entries
    that were clicked
    """
    if "name" not in session:
        return redirect(url_for("pages.login"))
    
    return render_template("history.html")

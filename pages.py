
from flask import Blueprint, render_template, url_for, redirect, request, session, flash
from models import db, Users, Movies_Shows, Favorites, History

pages = Blueprint("pages", __name__)

@pages.route("/")
def index():
    """
    route for homepage and serves as main directory for app containing links for relevant pages
    can be accessed without being signed in
    """

    return render_template("index.html")

@pages.app_errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@pages.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

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
    
    if user_db and user_db.check_password(password_input):
        flash("You are now logged in")
        session["name"] = user_db.username
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

    user_db = Users.query.filter_by(username=username_input).first()

    if user_db is None:
        flash("User is now registered")
        user = Users(username_input, password_input)
        db.session.add(user)
        db.session.commit()
    else:
        flash("User already exists")
        return redirect(url_for("pages.register"))
        
    return redirect(url_for("pages.login"))

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
     
    catalog = Movies_Shows.query.all()
    page_title = "Full Catalog"
    return render_template("list.html", catalog = catalog, page_title = page_title)

@pages.route("/list/<filter>+<name>")
def listFiltered(filter, name):
    """
    Finds entries from Movies_Shows model based on the provided filter type and name
    The function can query the database for entries that contain the provided name input, or
    it can filter by the given genre if the genre type filter is given
    """
    if "name" not in session:
        return redirect(url_for("pages.login"))
    
    filter_options = {
        "title": Movies_Shows.title.like(f"%{name}%"),
        "genre": Movies_Shows.genre == name
    }

    catalog = Movies_Shows.query.filter(filter_options[filter]).all()

    if (filter == "title"):
        page_title = "Search Results For: " + name
    elif(filter == "genre"):
        page_title = "Filtered By Genre: " + name

    return render_template("list.html", catalog=catalog, page_title = page_title)

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
    
    user = current_user()
    movie_show = Movies_Shows.query.filter_by(id=movies_shows_id).first()
    isFavorite = user.favorites.filter_by(movies_shows_id=movies_shows_id).first()

    history_entry = History(user.id, movies_shows_id)
    db.session.add(history_entry)
    db.session.commit()

    return render_template("detail.html", movie_show = movie_show, isFavorite = isFavorite)

@pages.route("/favoritesUpdate/<int:movies_shows_id>", methods=["POST"])
def favoritesUpdate(movies_shows_id):
    """
    Connected to favorites checkbox on the "/detail" page. When there is a change in the checkbox, it triggers
    the favoritesUpdate route which will take id and use it to add the entry to the user's favorites if it is 
    not already there, or it will remove it from the favorites if it already exists. The favorites update occurs
    in the backend, so page reloads and redirections are not needed, so the route returns an empty response and 
    not a template
    """
    if "name" not in session:
        return redirect(url_for("pages.login"))

    user = current_user()
    entry = user.favorites.filter_by(movies_shows_id=movies_shows_id).first()
    if (entry):
        db.session.delete(entry)
    else:
        db.session.add(Favorites(user.id, movies_shows_id))

    db.session.commit()
    return ""

@pages.route("/favorites")
def favorites():
    """
    route for favorites page that shows the list of favorites for the current user
    only accessible when logged in by checking if session has the "name" attribute
    """
    if "name" not in session:
        return redirect(url_for("pages.login"))
    
    user = current_user()
    favorites_ids = user.favorites.with_entities(Favorites.movies_shows_id)
    favorites_list = Movies_Shows.query.filter(Movies_Shows.id.in_(favorites_ids)).all()
    return render_template("list.html", catalog = favorites_list, page_title = "Favorites")


@pages.route("/history")
def history():
    """
    Displays a list of links using ids from the History table and titles from the
    Movies_Shows table to show the user their watch history
    """
    if "name" not in session:
        return redirect(url_for("pages.login"))
    
    user = current_user()

    history = History.query.filter_by(user_id = user.id).join(Movies_Shows, History.movies_shows_id == Movies_Shows.id).add_columns(History.movies_shows_id, Movies_Shows.title).all()
    history.reverse()

    return render_template("history.html", history = history)


def current_user():
    return Users.query.filter_by(username=session["name"]).first()
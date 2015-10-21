"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")

@app.route("/users")
def user_list():
    """Show list of users"""

    users = User.query.all()
    return render_template("users_list.html", users=users)

@app.route("/login")
def login_form():
    """Render login form"""

    return render_template("login.html")

@app.route("/login_submission", methods=["POST"])
def login_submission():
    """Confirms username and password through database and sessions."""
    # .get is safety net incase 'required' is removed from form in html
    # checks the forms dict which is nested inside the request dictionary
    email = request.forms.get("email")
    password = request.forms.get("password")
    user = User.query.filter(User.email == email).first()
    if user:
        # TODO check pw
        # 1 add user to session
        # flash message and them redirect "/"

    else:
        # add user and pw to database
        # flash message and them redirect "/"



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
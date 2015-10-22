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

@app.route("/users/<int:user_id>")
def user_info(user_id):
    """Shows information about a specific user."""

    user = User.query.filter(User.user_id == user_id).first()
    # list of rating objects with Rating attributes rating_id, movie_id, user_id, score
    ratings = user.ratings
    users_movie_ratings = []
    # for index in length rating list:
    # for i in ratings:
    #     count = len(range(ratings))
    # #  append to the users_movie_ratings list the movie title at index and the score at that index
        
    #     users_movie_ratings.append(ratings[count].movie.title + ratings[count].score)
    return render_template("user-info.html", user=user)

@app.route("/login")
def login_form():
    """Render login form"""

    return render_template("login.html")

@app.route("/login_submission", methods=["POST"])
def login_submission():
    """Confirms username and password through database and sessions."""
    # .get is safety net incase 'required' is removed from form in html
    # checks the forms dict which is nested inside the request dictionary
    email = request.form.get("email")
    password = request.form.get("password")
    user = User.query.filter(User.email == email).first()
    # if user in == True:
    if user:
        # TODO check pw
        if password == user.password:
        # 1 add user to session
            session["current_user"] = email
        # flash message 
            flash("Logged in as %s" % (email))
        # and them redirect "/"
            return redirect("/") 
        else:
            flash("Incorrect password submitted")
            return redirect("/login")  
    else:
        # add user and pw to database (instantiation of the class User), add and commit to the database
        new_user = User(email=email, password=password, age="NULL", zipcode="NULL")
        db.session.add(new_user)
        db.session.commit()
        # flash message 
        flash("New user logged in as %s" % (email))
        # and then redirect "/"
        return redirect("/")



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
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

@app.route('/movies')
def movie_list():
    """Shows list of movies"""

    movies = Movie.query.order_by(Movie.title).all()
    return render_template("movie-list.html", movies=movies )

@app.route("/movies/<int:movie_id>")
def movie_info(movie_id):
    """Show movie information and allow user to add or update rating"""

    movie = Movie.query.filter(Movie.movie_id == movie_id).first()
    ratings = movie.ratings

    movie_ratings = []

    for obj in ratings:
        movie_ratings.append(obj.score) 
      
    return render_template("movie-info.html", movie_ratings=movie_ratings, movie=movie)

@app.route("/rating_confirmation/<int:movie_id>", methods=["POST"])
def rating_confirmation(movie_id):
    """Adds or updates new movie rating to database"""

    score =request.form.get("score")
    user = session["current_user"]
    user_obj = User.query.filter(User.email == user).first()
    user_id = user_obj.user_id
    movie_obj = Movie.query.filter(Movie.movie_id == movie_id).first()
    title = movie_obj.title

    rating_obj = Rating.query.filter((Rating.user_id == user_id)
                                         & (Rating.movie_id == movie_id)).first()

    if rating_obj:
        # single_rating = rating_obj.query.filter(Movie.movie_id = movie_id).first()
        rating_obj.score = score
        db.session.commit()
        flash("Updated score for %s"%(title))
    else:   
        new_rating = Rating(movie_id=movie_id, user_id=user_id, score=score)
        db.session.add(new_rating)
        db.session.commit()

        flash("New score for %s" % (title))
    return redirect("/")

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
    # here we are finding the number of ratings and using that index get title and score
    for i in range(len(ratings)):
        users_movie_ratings.append(ratings[i].movie.title + str(ratings[i].score))
    # append to the users_movie_ratings list the movie title at index and the score at that index
    # for obj in ratings:
        # users_movie_ratings.append(obj.movie.title + str(obj.score))

    return render_template("user-info.html", user=user, users_movie_ratings=users_movie_ratings)

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
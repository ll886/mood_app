from flask import render_template, redirect, url_for, request, flash
from mood_app import app, db, bcrypt
from mood_app.forms import MoodForm, RegistrationForm, LoginForm
from mood_app.models import Mood, User
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime


@app.route("/")
def home():
    return render_template("home.html", title="Home")


@app.route("/mood", methods=["GET", "POST"])
# user needs to be logged in to access this page, will be redirected to login
@login_required
def mood():
    form = MoodForm()
    # when browser sends default GET request, form.validate_on_submit() will
    # returns false and just continues to render the template for the
    # mood.html
    # when browser sends POST request as a result of user submitting
    # the FlaskForm, it will return true after ensuring all the validators
    # set for each input field also is correct
    if form.validate_on_submit():
        mood = Mood(mood_value=form.mood_value.data, author=current_user)
        # add mood object to the database and commit it
        db.session.add(mood)
        db.session.commit()
        # message to indicate successful submission
        flash(
            "Your mood has been submitted successfully!", "success",
        )
        return redirect(url_for("mood"))
    # if no post request, returns mood.html
    # get all moods in the database
    # gets all the moods submitted for the user logged in
    moods = current_user.moods
    streak = None
    if len(moods) != 0:
        streak = get_streak(moods)
    return render_template(
        "mood.html", form=form, moods=moods, title="Moods", streak=streak
    )


def get_streak(moods):
    streak = 0
    # reverse list to sort moods by newest to oldest
    # compares dates of submitted moods and find streak of consecutive days
    moods.reverse()
    date_to_compare = moods[0].date_posted.date()
    # if latest mood's date was not today or yesterday
    # the streak has broken and resets back to 0
    # otherwise, check how many days the user has consecutively submitted a mood
    if is_consecutive(datetime.today(), date_to_compare):
        # since the latest mood date is either today/yesterday, streak is at least 1
        streak += 1
        for mood in moods:
            date_of_mood = mood.date_posted.date()
            if date_of_mood == date_to_compare:
                # if user posts multiple moods on same day
                # do nothing to the streak
                continue
            elif is_consecutive(date_to_compare, date_of_mood):
                streak += 1
                date_to_compare = date_of_mood
            else:
                # there is a gap between days, break out of loop
                break
    else:
        return 0
    return streak


def is_consecutive(date1, date2):
    # returns true if the year, month is the same and also if
    # the day is the same or if the date2 is only 1 day behind date1
    if (
        date1.year == date2.year
        and date1.month == date2.month
        and date1.day - date2.day == 1
        or date1.day == date2.day
    ):
        return True
    return False


@app.route("/register", methods=["GET", "POST"])
def register():
    # if user tries to navigate to '/register' while logged in, redirect back to home
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    # returns true when POSTed and validators are all correct for the form
    if form.validate_on_submit():
        # create a hashed password as a string with bcrypt for security
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        # create new user object with form email data and hashed password
        new_user = User(email=form.email.data, password=hashed_password)
        # add to database and commit
        db.session.add(new_user)
        db.session.commit()
        # flash message for next page to indicate success
        flash(
            "You have successfully created an account. You can now log in.", "success"
        )
        return redirect(url_for("login"))
    # returns the register.html as the default GET request and pass the form
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    # if user tries to navigate to '/home' while logged in, redirect back to hom
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    # returns true when POSTed and validators are all correct for the form
    if form.validate_on_submit():
        # gets the user for the corresponding email submitted by user
        # attempts to match the form password and password for the user
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # if passwords match, call the login_user function
            login_user(user, remember=form.remember.data)
            # after successful login, navigate to back to home
            # or mood page if user was trying to access it and was redirected to login
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash(
                "Login was unsuccessful. Incorrect Information or user does not exist",
                "danger",
            )
    # return login.html as default GET request, pass login form
    return render_template("login.html", title="Login", form=form)


@app.route("/logout")
def logout():
    # calls the logout_user function and redirect back to home
    logout_user()
    return redirect(url_for("home"))


@app.route("/post/<int:mood_id>/delete", methods=["POST"])
@login_required
def delete_mood(mood_id):
    mood = Mood.query.get_or_404(mood_id)
    # gets the mood at the specified id
    if mood.author != current_user:
        abort(403)
    # delete mood and commit change
    db.session.delete(mood)
    db.session.commit()
    flash("You have successfully deleted this mood", "success")
    return redirect(url_for("mood"))

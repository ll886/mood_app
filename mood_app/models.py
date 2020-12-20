from mood_app import db, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Mood model
class Mood(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mood_value = db.Column(db.Integer, nullable=False)
    # date posted is the current time
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"Mood('mood_value: {self.mood_value}')"


# User Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    moods = db.relationship("Mood", backref="author", lazy=True)

    def __repr__(self):
        return f"User('mood_value: {self.email}')"

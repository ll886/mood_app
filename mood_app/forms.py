from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, StringField, BooleanField, PasswordField
from wtforms.validators import (
    DataRequired,
    NumberRange,
    Email,
    EqualTo,
    ValidationError,
    Length,
)
from mood_app.models import User
from flask_login import current_user


class MoodForm(FlaskForm):
    # mood values on a scale from 1 to 10, inclusive
    mood_value = IntegerField(
        "Mood Value",
        validators=[
            DataRequired(),
            NumberRange(min=1, max=10, message="Mood value must be between 1 and 10"),
        ],
    )
    submit = SubmitField("Submit Mood")


# Register and Login Forms
# users will register with email
class RegistrationForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), Length(min=6), EqualTo("password")],
    )
    submit = SubmitField("Sign Up")

    # will check if there are any other emails with the same email
    # entered while user is registering
    def validate_email(self, email):
        # tries to retrieve a user with the email submitted
        user = User.query.filter_by(email=email.data).first()
        # if user exist and is not None, raise validation error
        if user:
            raise ValidationError(
                "There is already an account registered with the email. Please choose another."
            )


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")

from flask_wtf import FlaskForm  # Import the FlaskForm class from the flask_wtf module.
from wtforms import StringField, PasswordField, SubmitField, TextAreaField  # Import specific fields from the wtforms module.
from wtforms.validators import DataRequired, Email, Length  # Import specific validators from the wtforms.validators module.

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])  # Create a StringField for the username with validators for required data and length constraints.
    password = PasswordField('Password', validators=[DataRequired()])  # Create a PasswordField for the password with a validator for required data.
    email = StringField('Email', validators=[DataRequired(), Email()])  # Create a StringField for the email with validators for required data and email format.
    first_name = StringField('First Name', validators=[DataRequired()])  # Create a StringField for the first name with a validator for required data.
    last_name = StringField('Last Name', validators=[DataRequired()])  # Create a StringField for the last name with a validator for required data.
    submit = SubmitField('Register')  # Create a SubmitField with the label "Register".

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])  # Create a StringField for the username with validators for required data and length constraints.
    password = PasswordField('Password', validators=[DataRequired()])  # Create a PasswordField for the password with a validator for required data.
    submit = SubmitField('Login')  # Create a SubmitField with the label "Login".

class FeedbackForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])  # Create a StringField for the title with validators for required data and length constraint.
    content = TextAreaField('Content', validators=[DataRequired()])  # Create a TextAreaField for the content with a validator for required data.
    submit = SubmitField('Submit')  # Create a SubmitField with the label "Submit".

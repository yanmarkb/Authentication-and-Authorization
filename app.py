
# Import necessary modules and packages
from flask import Flask, render_template, redirect, session, flash
from forms import RegisterForm, LoginForm, FeedbackForm
from models import db, User, Feedback
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from flask_bcrypt import Bcrypt

# Create Flask application instance
app = Flask(__name__)

# Initialize Bcrypt for password hashing
bcrypt = Bcrypt(app)

# Configure Flask application settings
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask_feedback_db'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# Initialize Debug Toolbar extension
debug = DebugToolbarExtension(app)

# Initialize SQLAlchemy database
db.init_app(app)

# Create database tables before the first request
@app.before_first_request
def create_tables():
    db.create_all()

# Define home route
@app.route('/')
def home():
    # Redirect to the registration page
    return redirect('/register')

# Define registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Create an instance of the registration form
    form = RegisterForm()
    if form.validate_on_submit():
        # Hash the password and create a new user
        hashed_password = User.hash_password(form.password.data)
        user = User(
            username=form.username.data, 
            password=hashed_password,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data 
        )
        # Add the user to the database and commit the changes
        db.session.add(user)
        db.session.commit()
        # Store the username in the session and redirect to the user's page
        session['username'] = user.username
        return redirect('/users/' + user.username)  
    # Render the registration form template
    return render_template('register.html', form=form)

# Define login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Create an instance of the login form
    form = LoginForm()
    if form.validate_on_submit():
        # Check if the username and password are correct
        user = User.query.filter_by(username=form.username.data).first()
        if user and User.check_password(user.password, form.password.data):
            # Store the username in the session and redirect to the user's page
            session['username'] = user.username
            return redirect('/users/' + user.username)
        # Display an error message if the username or password is incorrect
        flash('Wrong username or password')
    # Render the login form template
    return render_template('login.html', form=form)

# Define user page route
@app.route('/users/<username>') 
def user_page(username):
    # Check if the user is logged in and the username matches the session
    if 'username' not in session or session['username'] != username: 
        # Redirect to the login page
        return redirect('/login')
    # Get the user and their feedbacks from the database
    user = User.query.filter_by(username=username).first()
    feedbacks = Feedback.query.filter_by(username=username).all()
    # Render the user page template with the user and their feedbacks
    return render_template('user.html', user=user, feedbacks=feedbacks)  

# Define delete user route
@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    # Check if the user is logged in and the username matches the session
    if 'username' not in session or session['username'] != username: 
        # Redirect to the login page
        return redirect('/login')
    # Delete the user from the database
    User.query.filter_by(username=username).delete()
    db.session.commit()
    # Clear the session and redirect to the home page
    session.clear()
    return redirect('/')

# Define add feedback route
@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def add_feedback(username):
    # Check if the user is logged in and the username matches the session
    if 'username' not in session or session['username'] != username: 
        # Redirect to the login page
        return redirect('/login')
    # Create an instance of the feedback form
    form = FeedbackForm()
    if form.validate_on_submit():
        # Create a new feedback and add it to the database
        feedback = Feedback(title=form.title.data, content=form.content.data, username=username)
        db.session.add(feedback)
        db.session.commit()
        # Redirect to the user's page
        return redirect(f'/users/{username}')
    # Render the feedback add form template
    return render_template('feedback_add.html', form=form)

# Define update feedback route
@app.route('/feedback/<int:feedback_id>/update', methods=['GET', 'POST'])
def update_feedback(feedback_id):
    # Get the feedback by its ID or return a 404 error if not found
    feedback = Feedback.query.get_or_404(feedback_id)
    # Check if the user is logged in and the username matches the session
    if 'username' not in session or session['username'] != feedback.username: 
        # Redirect to the login page
        return redirect('/login')
    # Create an instance of the feedback form with the existing feedback data
    form = FeedbackForm(obj=feedback)
    if form.validate_on_submit():
        # Update the feedback with the new data and commit the changes
        feedback.title = form.title.data
        feedback.content = form.content.data
        db.session.commit()
        # Redirect to the user's page
        return redirect(f'/users/{feedback.username}')
    # Render the feedback edit form template
    return render_template('feedback_edit.html', form=form, feedback=feedback)

# Define delete feedback route
@app.route('/feedback/<int:feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    # Get the feedback by its ID or return a 404 error if not found
    feedback = Feedback.query.get_or_404(feedback_id)
    # Check if the user is logged in and the username matches the session
    if 'username' not in session or session['username'] != feedback.username: 
        # Redirect to the login page
        return redirect('/login')
    # Delete the feedback from the database
    db.session.delete(feedback)
    db.session.commit()
    # Redirect to the user's page
    return redirect(f'/users/{feedback.username}')

# Define logout route
@app.route('/logout')
def logout():
    """Clear any information from the session and redirect to /"""
    # Clear the session and display a flash message
    session.clear()
    flash("See you later!")
    # Redirect to the home page
    return redirect('/')


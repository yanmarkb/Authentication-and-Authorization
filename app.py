from flask import Flask, render_template, redirect, session, flash
from forms import RegisterForm, LoginForm, FeedbackForm
from models import db, User, Feedback
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from flask_bcrypt import Bcrypt

app = Flask(__name__)

bcrypt = Bcrypt(app)

app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask_feedback_db'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def home():
    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = User.hash_password(form.password.data)
        user = User(
            username=form.username.data, 
            password=hashed_password,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data 
        )
        db.session.add(user)
        db.session.commit()
        session['username'] = user.username
        return redirect('/users/' + user.username)  
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and User.check_password(user.password, form.password.data):
            session['username'] = user.username
            return redirect('/users/' + user.username)
        flash('Wrong username or password')
    return render_template('login.html', form=form)

@app.route('/users/<username>') 
def user_page(username):
    if 'username' not in session or session['username'] != username: 
        return redirect('/login')
    user = User.query.filter_by(username=username).first()
    feedbacks = Feedback.query.filter_by(username=username).all()
    return render_template('user.html', user=user, feedbacks=feedbacks)  

@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    if 'username' not in session or session['username'] != username: 
        return redirect('/login')
    User.query.filter_by(username=username).delete()
    db.session.commit()
    session.clear()
    return redirect('/')

@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def add_feedback(username):
    if 'username' not in session or session['username'] != username: 
        return redirect('/login')
    form = FeedbackForm()
    if form.validate_on_submit():
        feedback = Feedback(title=form.title.data, content=form.content.data, username=username)
        db.session.add(feedback)
        db.session.commit()
        return redirect(f'/users/{username}')
    return render_template('feedback_add.html', form=form)

@app.route('/feedback/<int:feedback_id>/update', methods=['GET', 'POST'])
def update_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    if 'username' not in session or session['username'] != feedback.username: 
        return redirect('/login')
    form = FeedbackForm(obj=feedback)
    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        db.session.commit()
        return redirect(f'/users/{feedback.username}')
    return render_template('feedback_edit.html', form=form, feedback=feedback)

@app.route('/feedback/<int:feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    if 'username' not in session or session['username'] != feedback.username: 
        return redirect('/login')
    db.session.delete(feedback)
    db.session.commit()
    return redirect(f'/users/{feedback.username}')

@app.route('/logout')
def logout():
    """Clear any information from the session and redirect to /"""
    session.clear()
    return redirect('/')
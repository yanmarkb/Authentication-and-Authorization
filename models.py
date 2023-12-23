from flask_sqlalchemy import SQLAlchemy  # Import the SQLAlchemy module for working with databases.
from flask_bcrypt import Bcrypt  # Import the Bcrypt module for password hashing.

db = SQLAlchemy()  # Create an instance of the SQLAlchemy class.

class User(db.Model):  # Define a User class that represents a table in the database.
    __tablename__ = 'users'  # Set the table name to 'users'.

    username = db.Column(db.String(20), primary_key=True)  # Define a column 'username' with a maximum length of 20 characters and set it as the primary key.
    password = db.Column(db.Text, nullable=False)  # Define a column 'password' with a text data type and make it non-nullable.
    email = db.Column(db.String(50), nullable=False, unique=True)  # Define a column 'email' with a maximum length of 50 characters, make it non-nullable, and enforce uniqueness.
    first_name = db.Column(db.String(30), nullable=False)  # Define a column 'first_name' with a maximum length of 30 characters and make it non-nullable.
    last_name = db.Column(db.String(30), nullable=False)  # Define a column 'last_name' with a maximum length of 30 characters and make it non-nullable.

    @classmethod
    def hash_password(cls, password):  # Define a class method 'hash_password' that takes a password as input.
        bcrypt = Bcrypt()  # Create an instance of the Bcrypt class.
        return bcrypt.generate_password_hash(password).decode('utf-8')  # Hash the password using Bcrypt and return the hashed password as a string.

    @classmethod
    def check_password(cls, hashed_password, password):  # Define a class method 'check_password' that takes a hashed password and a password as input.
        bcrypt = Bcrypt()  # Create an instance of the Bcrypt class.
        return bcrypt.check_password_hash(hashed_password, password)  # Check if the provided password matches the hashed password and return a boolean value.

    @classmethod
    def authenticate(cls, username, password):  # Define a class method 'authenticate' that takes a username and a password as input.
        user = cls.query.filter_by(username=username).first()  # Query the database for a user with the provided username.
        if user and cls.check_password(user.password, password):  # If a user is found and the provided password matches the user's hashed password:
            return user  # Return the user object.
        else:
            return False  # Otherwise, return False.

class Feedback(db.Model):  # Define a Feedback class that represents a table in the database.
    __tablename__ = 'feedback'  # Set the table name to 'feedback'.

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Define a column 'id' with an integer data type, set it as the primary key, and enable auto-increment.
    title = db.Column(db.String(100), nullable=False)  # Define a column 'title' with a maximum length of 100 characters and make it non-nullable.
    content = db.Column(db.Text, nullable=False)  # Define a column 'content' with a text data type and make it non-nullable.
    username = db.Column(db.String(20), db.ForeignKey('users.username'))  # Define a column 'username' with a maximum length of 20 characters and set it as a foreign key referencing the 'username' column in the 'users' table.

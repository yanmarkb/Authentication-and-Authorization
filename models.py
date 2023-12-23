from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt



db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    @classmethod
    def hash_password(cls, password):
        bcrypt = Bcrypt()
        return bcrypt.generate_password_hash(password).decode('utf-8')

    @classmethod
    def check_password(cls, hashed_password, password):
        bcrypt = Bcrypt()
        return bcrypt.check_password_hash(hashed_password, password)
    @classmethod
    def authenticate(cls, username, password):
        user = cls.query.filter_by(username=username).first()
        if user and cls.check_password(user.password, password):
            return user
        else:
            return False

class Feedback(db.Model):
    __tablename__ = 'feedback'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(db.String(20), db.ForeignKey('users.username'))

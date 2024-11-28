from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
import hashlib
import bcrypt
# from app import app

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_1.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy db with the Flask app
db = SQLAlchemy(app)

# User Model
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    # scores = db.relationship('Score', backref='user', lazy=True)

    def __init__(self, email, password_hash):
        self.email = email
        self.password_hash = self.hash_password(password_hash)

    # def verify_password(self, password):
    #     return check_password_hash(self.password_hash, password)
    
    def verify_password(self, password, hashed_password):
        # Hash the provided password and compare it with the stored hash
        print(password, hashed_password)
        return self.hash_password(password) == hashed_password

    def get_id(self):
        return self.user_id
    
    def hash_password(self, password):
        return hashlib.sha256((password).encode()).hexdigest()

    def check_password(hashed_password, user_input):
        return bcrypt.checkpw(user_input.encode('utf-8'), hashed_password  .encode('utf-8'))


# Category Model
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    
    def __init__(self, name):
        self.name = name

# Question Model
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(255), nullable=False)
    options = db.Column(db.String, nullable=False)  # Store options as a JSON string
    correct_answer = db.Column(db.String(255), nullable=False)
    category_id = db.Column(db.Integer, nullable=False)

    def __init__(self, question, options, correct_answer, category_id):
        self.question = question
        self.options = options
        self.correct_answer = correct_answer
        self.category_id = category_id

# Score Model
class Score(db.Model):
    __tablename__ = 'score'
    score_id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    # quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    # date_submitted = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    # quiz = db.relationship('Quiz', backref='scores')
    
    # CREATE CONSTRUCTOR FOR SCORE LIKE ABOVE def __init__
    def __init__(self, score, user_id):
        self.score = score
        self.user_id = user_id
    
class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref='quizzes')

# Create the database tables
with app.app_context():
    db.create_all()

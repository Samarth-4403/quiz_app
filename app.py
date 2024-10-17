from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import db, Question, Category, User, Score
from werkzeug.security import generate_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import logging
from auth import auth  # Import the auth Blueprint

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = '0123456789'
app.register_blueprint(auth, url_prefix='/auth')  # Register the blueprint

app.logger.setLevel(logging.DEBUG)
# Initialize DB
db.init_app(app)  # Only initialize SQLAlchemy here

# Initialize Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Load user for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@login_required
def index():
    categories = Category.query.all()
    return render_template('index.html', categories=categories)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user and user.verify_password(password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        else:
            flash('Invalid email or password')
            return redirect('/login')

    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    password = request.form['password']
    hashed_password = generate_password_hash(password)

    # Check if the user already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return "User with this email already exists!"

    # If user doesn't exist, create a new one
    new_user = User(email=email, password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return "User registered successfully!"

@app.route('/check_user')
def check_user():
    user = User.query.filter_by(email='test@example.com').first()
    if user:
        return f"User: {user.email}, Password Hash: {user.password_hash}"
    else:
        return "User not found"

@app.route('/check_password')
def check_password():
    user = User.query.filter_by(email="test@example.com").first()
    if user:
        return f"Password Hash: {user.password_hash}, Correct: {user.verify_password('password123')}"
    return "User not found"

@app.route('/quiz/<int:category_id>')
@login_required
def quiz(category_id):
    session['quiz_started'] = True
    questions = Question.query.filter_by(category_id=category_id).all()
    return render_template('quiz.html', questions=questions)

@app.route('/result/<int:score>', methods=['GET'])  # Add the score as URL parameter
@login_required
def result(score):
    return render_template('result.html', score=score)

@app.route('/submit_quiz', methods=['POST'])
@login_required
def submit_quiz():
    correct = 0
    total = 0
    for question_id, user_answer in request.form.items():
        question = Question.query.get(int(question_id))
        if question and question.correct_answer == user_answer:
            correct += 1
        total += 1
    
    score = int((correct / total) * 100)
    
    # Save the score in the database
    new_score = Score(user_id=current_user.user_id, score=score)
    db.session.add(new_score)
    db.session.commit()
    
    session.pop('quiz_started', None)

    return redirect(url_for('result', score=score))

@app.route('/result', methods=['POST'])
@login_required
def quiz_result():
    correct = 0
    total = 0
    for question_id, answer in request.form.items():
        question = Question.query.get(int(question_id))
        if question and question.correct_answer == answer:
            correct += 1
        total += 1
    return render_template('result.html', correct=correct, total=total)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    scores = Score.query.filter_by(user_id=current_user.user_id).all()
    return render_template('dashboard.html', scores=scores)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

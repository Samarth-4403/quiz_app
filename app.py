from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from models import db, Question, Category, User, Score
from werkzeug.security import generate_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import logging
from auth import auth
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_1.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = '0123456789'
app.register_blueprint(auth, url_prefix='/auth')  # Register the blueprint
# db = SQLAlchemy(app)

app.logger.setLevel(logging.DEBUG)
# Initialize DB
db.init_app(app) 

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
    questions = Question.query.all()
    print(questions)
    questions_data = []
    for q in questions:
        # Deserialize the options field from JSON string to list
        options_list = json.loads(q.options)
        # print(options_list, type(options_list))
        questions_data.append({
            'question': q.question,
            'id': q.id,
            'options': options_list,
            'correct_answer': q.correct_answer
        })
    return render_template('index.html', categories=categories, questions=questions_data)

@app.route('/submit_answers', methods=['POST'])
def submit_answers():
    if request.method == 'POST':
        # Iterate over each question and retrieve the selected answer
        count = 0
        for ques in Question.query.all():
            selected_answer = request.form.get(f"answer_{ques.id}")
            print(selected_answer, "id")
            if selected_answer == ques.correct_answer:
                count += 1
        # s = Score(count,session['user_id']) # Commit 62-64 lines if error occurs after constructor in Score model
        # db.session.add(s)
        # db.session.commit()
    return render_template('result.html', score = count)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        print(email, password)
        user = User.query.filter_by(email=email).first()
        session['user_id'] = user.user_id
        print(user.password_hash)
        if user and user.verify_password(password, user.password_hash):
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
    session.pop('quiz_submitted', None)  # Reset submission status
    session['quiz_started'] = True
    questions = Question.query.filter_by(category_id=category_id).all()
    return render_template('quiz.html', questions=questions)

def get_quiz_id():
    return request.form.get('quiz_id')

@app.route('/result/<int:score>', methods=['GET'])  # Add the score as URL parameter
@login_required
def result(score):
    return render_template('result.html', score=score)

@app.route('/submit_quiz', methods=['POST'])
@login_required
def submit_quiz():
    if 'quiz_submitted' in session:  # Check if the quiz was already submitted
        flash('You have already submitted this quiz.')
        return redirect(url_for('dashboard'))

    correct = 0
    total = 0
    for question_id, user_answer in request.form.items():
        question = Question.query.get(int(question_id))
        if question and question.correct_answer == user_answer:
            correct += 1
        total += 1

    score = int((correct / total) * 100)

    # Save the score in the database
    new_score = Score(user_id=current_user.get_id(), score=score, quiz_id=1)  # Update with proper `quiz_id`
    db.session.add(new_score)
    db.session.commit()

    # Mark quiz as submitted in session
    session['quiz_submitted'] = True

    flash('Quiz submitted successfully.')
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

@app.route('/submit_score', methods=['POST'])
def submit_score():
    data = request.get_json()
    score = data['score']
    user_id = current_user.id  # Assuming you have user authentication

    # Create a new Score object and save it to the database
    new_score = Score(user_id=user_id, score=score)
    db.session.add(new_score)
    db.session.commit()

    return jsonify({'message': 'Score submitted successfully'})

# Route to update score
@app.route('/update_score', methods=['POST'])
def update_score():
    # Get data from the request body (adjust based on your request format)
    data = request.get_json()
    user_id = data.get('user_id')
    quiz_id = data.get('quiz_id')
    new_score = data.get('score')

    # Validate data (optional, you can add more checks)
    if not user_id or not quiz_id or not new_score:
        return jsonify({'error': 'Missing required fields'}), 400

    # Check if a score entry already exists for this user and quiz
    existing_score = Score.query.filter_by(user_id=user_id, quiz_id=quiz_id).first()

    # Update existing score if found, otherwise create a new entry
    if existing_score:
        existing_score.score = new_score
    else:
        new_score_entry = Score(score=new_score, user_id=user_id, quiz_id=quiz_id)
        db.session.add(new_score_entry)

    # Save changes to the database
    db.session.commit()

    return jsonify({'message': 'Score updated successfully'}), 200

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    try:
        scores = Score.query.filter_by(user_id=current_user.get_id()).all()
        if scores:
            return render_template('dashboard.html', scores=scores)
        else:
            flash("No scores found for this user.")
            return render_template('dashboard.html', scores=[])
    except Exception as e:
        print(f"Error retrieving scores: {e}")
        flash("An error occurred while fetching your scores. Please try again later.")
        return render_template('dashboard.html', scores=[])


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

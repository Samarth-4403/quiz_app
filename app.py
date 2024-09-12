from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import db, Question, Category, User
from werkzeug.security import check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = '0123456789'

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

@app.route('/quiz/<int:category_id>')
@login_required
def quiz(category_id):
    questions = Question.query.filter_by(category_id=category_id).all()
    return render_template('quiz.html', questions=questions)

@app.route('/result', methods=['POST'])
@login_required
def result():
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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for, session 
from models import db, Question, Category

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = '0123456789'

db.init_app(app)

@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))  # Redirect to login if not authenticated
    categories = Category.query.all()
    return render_template('index.html', categories=categories)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        # Set new user in session
        session['username'] = username
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/quiz/<int:category_id>')
def quiz(category_id):
    if 'username' not in session:
        return redirect(url_for('login'))  # Redirect to login if not authenticated
    questions = Question.query.filter_by(category_id=category_id).all()
    return render_template('quiz.html', questions=questions)

@app.route('/result', methods=['POST'])
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
def logout():
    session.pop('username', None)  # Remove 'username' from session
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

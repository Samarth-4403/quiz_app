from flask import Flask, render_template, request, redirect, url_for
from models import db, Question, Category

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
def index():
    categories = Category.query.all()
    return render_template('index.html', categories=categories)

@app.route('/quiz/<int:category_id>')
def quiz(category_id):
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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

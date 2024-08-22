from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app import db
from models import Quiz, Question

bp = Blueprint('quiz', __name__, url_prefix='/quiz')

@bp.route('/')
@login_required
def index():
    quizzes = Quiz.query.all()
    return render_template('quiz/index.html', quizzes=quizzes)

@bp.route('/<int:quiz_id>')
@login_required
def take_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    return render_template('quiz/quiz.html', quiz=quiz)

@bp.route('/<int:quiz_id>/submit', methods=['POST'])
@login_required
def submit_quiz(quiz_id):
    # Process quiz submission here
    return redirect(url_for('quiz.index'))

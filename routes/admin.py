from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app import db
from models import Quiz, Question

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/')
@login_required
def dashboard():
    if current_user.role != 'Admin':
        return redirect(url_for('index'))
    quizzes = Quiz.query.all()
    return render_template('admin/dashboard.html', quizzes=quizzes)

@bp.route('/quiz/new', methods=['GET', 'POST'])
@login_required
def new_quiz():
    if current_user.role != 'Admin':
        return redirect(url_for('index'))
    if request.method == 'POST':
        title = request.form['title']
        quiz = Quiz(title=title)
        db.session.add(quiz)
        db.session.commit()
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/new_quiz.html')

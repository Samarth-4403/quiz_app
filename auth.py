from flask import Blueprint, render_template, redirect, url_for, flash
from forms import LoginForm
from models import User
from flask_bcrypt import Bcrypt
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash

bcrypt = Bcrypt()
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        # Query user from database
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password')
    return render_template('login.html', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

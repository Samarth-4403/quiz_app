from flask import Blueprint, render_template, redirect, url_for, flash, session
from forms import LoginForm
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
auth = Blueprint('auth', __name__)

# Temporary user data
users = {'user1': bcrypt.generate_password_hash('password123').decode('utf-8')}

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        # Check if user exists and password is correct
        if username in users and bcrypt.check_password_hash(users[username], password):
            session['username'] = username
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check your credentials.')
    return render_template('login.html', form=form)

@auth.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

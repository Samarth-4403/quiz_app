from flask import Flask, render_template  
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from models import User
from db import db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
@app.route('/')
def index():
    return render_template('index.html')
    #return 'Hello' 

from routes import auth, quiz, admin
app.register_blueprint(auth.bp)
app.register_blueprint(quiz.bp)
app.register_blueprint(admin.bp)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

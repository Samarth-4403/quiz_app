from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)

from routes import auth, quiz, admin
app.register_blueprint(auth.bp)
app.register_blueprint(quiz.bp)
app.register_blueprint(admin.bp)

if __name__ == '__main__':
    app.run(debug=True)

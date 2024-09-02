from app import app, db
from models import Category, Question

def add_data():
    category1 = Category(name="Python")
    category2 = Category(name="JavaScript")

    question1 = Question(
        text="What is the capital of France?",
        options=["Paris", "Berlin", "Rome", "Madrid"],
        correct_answer="Paris",
        category=category1
    )
    question2 = Question(
        text="What does HTML stand for?",
        options=["HyperText Markup Language", "HighText Machine Language", "HyperLoop Machine Language", "None of the above"],
        correct_answer="HyperText Markup Language",
        category=category2
    )

    db.session.add(category1)
    db.session.add(category2)
    db.session.add(question1)
    db.session.add(question2)
    db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        add_data()

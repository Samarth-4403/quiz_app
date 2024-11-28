from app import db, app
from models import Question  # Assuming you have a Question model defined
import json  # To serialize the options as a JSON string


# Data to insert
questions = [
    {
        "question": "What is the output of print(2 ** 3)?",
        "options": ["5", "6", "8", "9"],
        "correct_answer": "8",
        "category_id": 1  # category_id should be an integer
    },
    {
        "question": "Which of the following is a valid variable name in Python?",
        "options": ["2abc", "_abc", "def", "for"],
        "correct_answer": "_abc",
        "category_id": 1  # category_id should be an integer
    },
    {
        "question": "What is the output of print(type([]))?",
        "options": ["<class 'list'>", "<class 'tuple'>", "<class 'dict'>", "<class 'set'>"],
        "correct_answer": "<class 'list'>",
        "category_id": 1  # category_id should be an integer
    },
    {
        "question": "Which keyword is used for function declaration in Python?",
        "options": ["function", "void", "def", "lambda"],
        "correct_answer": "def",
        "category_id": 1  # category_id should be an integer
    },
    {
        "question": "What does the 'len()' function do in Python?",
        "options": ["Calculates length", "Returns last element", "Sorts items", "Generates sequence"],
        "correct_answer": "Calculates length",
        "category_id": 1  # category_id should be an integer
    }
]

# Insert data
def populate_question():       
    for question_data in questions:
        # Serialize options as a JSON string
        options_json = json.dumps(question_data["options"])

        # Create a Question object and add it to the session
        ques = Question(
            question=question_data["question"],
            options=options_json,  # Store options as a JSON string
            correct_answer=question_data["correct_answer"],
            category_id=question_data["category_id"]
        )
        db.session.add(ques)

    # Commit once after adding all questions
    db.session.commit()
    print("Questions added successfully!")

    # Optionally, print each question added (for debugging or logging)
    for question in questions:
        print(question)

print("questions")

with app.app_context():
    # populate_question()
    questions = Question.query.all()
    for q in questions:
        print (q)
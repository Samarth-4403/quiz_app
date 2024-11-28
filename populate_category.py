from app import db, app
from models import Category, User  # Assuming you have a Question model defined
import json  # To serialize the options as a JSON string

categories = [
    "python", "golang", "java", "C", "php"
]
with app.app_context():
    
    # for category in categories:
    #     x = Category(category) 
    #     db.session.add(x)
        
    # db.session.commit()
    
    categories = Category.query.all()
    for category in categories:
        print(category.name)
        
users = [
    {"user": "User_1@example.com",
     "password":"password123"}, 
    {"user": "User_2@example.com",
     "password":"password456"}   
] 
with app.app_context():
    
    for user in users:
        y = User(user.get("user"),user.get("password"))
        print(user.get("user"),user.get("password"))
        db.session.add(y)
    db.session.commit()
    
        
        
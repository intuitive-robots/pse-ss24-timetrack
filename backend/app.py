import logging
from urllib.parse import quote

from flask import Flask, jsonify
from pymongo import MongoClient
from model.personal_information import PersonalInfo
from model.user import User
from db import initialize_db, check_db_connection

username = "admin"
password = "TimeTracking123!"
encoded_password = quote(password)

app = Flask(__name__)
db = initialize_db()


@app.route('/')
def home():
    return "Flask Backend"


"""
Creates a test user in the database
"""
@app.route('/create_testUser')
def create_user():
    # Create a new user document and save it in the database
    user = User(
        username="test_user",
        password_hash="test_password",
        personal_info=PersonalInfo(
            first_name="John",
            last_name="Doe",
            email="test@gmail.com",
            personal_number="123456",
            instituteName="Test Institute"),
        role=UserRole.ADMIN
    )
    user.save()
    return "User created"


"""
Searches for a test user in the database and returns it as a JSON object
"""
@app.route('/find_user_by_username')
def find_user_by_username():
    user = User.find_by_username("test_user")
    return jsonify(user.to_dict())


"""
Reads all users in the database and returns them as a JSON object
"""
@app.route('/read_users')
def read_users():
    # Read all users from the database and return them as a string
    all_users = list(db.users.find())
    return str(all_users)


"""
Checks the connection to the MongoDB database
"""
@app.route('/check_mongoDB_connection')
def check_mongoDB_connection():
    return check_db_connection()


if __name__ == '__main__':
    app.run(debug=True)

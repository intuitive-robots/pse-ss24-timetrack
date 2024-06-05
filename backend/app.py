from flask import Flask, jsonify
from model.personalInformation import PersonalInfo
from model.role import UserRole
from model.user import User
from db import initializeDb, checkDbConnection
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from datetime import timedelta
from auth import initAuthRoutes, check_access
import secrets
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # enable CORS for all routes and origins
db = initializeDb()

app.config["JWT_SECRET_KEY"] = secrets.token_bytes(32)  # Generates a random secret key
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=12)
jwt = JWTManager(app)

initAuthRoutes(app)


@app.route('/')
def home():
    return "Flask Backend"

def user_to_dict(user):
    user['_id'] = str(user['_id'])  # Convert ObjectId to string
    return user


@app.route('/createTestUser')
@jwt_required()
def createUser():
    """
    Creates a test user in the database
    TODO: This is a hardcoded user, replace this with a React form
    :return: A string indicating that the user was created
    """
    user = User(
        username="testads1s",
        passwordHash="test_password",
        personalInfo=PersonalInfo(
            firstName="John",
            lastName="Doe",
            email="test@gmail.com",
            personalNumber="123456",
            instituteName="Test Institute"),
        role=UserRole.ADMIN
    )
    user.save()
    return "User created"

@app.route('/readUsers')
@jwt_required()
@check_access(roles=[UserRole.ADMIN])
def readUsers():
    """
    Reads all users from the database
    Is only accessible to users with the role ADMIN
    :return: A JSON string containing all users
    """
    all_users = list(db.users.find())
    all_users = [user_to_dict(user) for user in all_users]
    return jsonify(all_users)


@app.route('/checkMongoDBConnection')
def checkMongodbConnection():
    """
    Check the connection to the MongoDB database
    :return: A string indicating the connection status
    """
    return checkDbConnection()


if __name__ == '__main__':
    app.run(debug=True)

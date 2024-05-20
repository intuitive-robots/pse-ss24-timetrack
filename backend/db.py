from flask_pymongo import PyMongo

mongo = None

def initialize_db(app):
    global mongo
    mongo = PyMongo(app)

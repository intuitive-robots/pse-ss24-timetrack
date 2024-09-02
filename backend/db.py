import os

from pymongo import MongoClient

db = None
client = None


def initialize_db():
    """
    Initializes the database connection
    """
    global db
    global client

    db_host = os.getenv('DB_HOST', 'localhost') # Get the DB_HOST environment variable or use 'localhost' as default
    client = MongoClient(db_host, 27017, username='admin', password='TimeTracking123!')
    db = client.timetracking_db_production
    return db


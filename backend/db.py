from pymongo import MongoClient

db = None
client = None


def initialize_db():
    """
    Initializes the database connection
    """
    global db
    global client

    client = MongoClient('158.180.40.137', 27017, username='admin', password='TimeTracking123!')
    db = client.timetracking_db_presentation
    return db


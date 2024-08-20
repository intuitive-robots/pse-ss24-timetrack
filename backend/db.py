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
    # TODO: Hard coding is usually not a good idea. We could use environment variables instead, when we have time.
    # TODO: For deployment, we should change the IP to localhost
    #client = MongoClient('158.180.40.137', 27017, username='admin', password='TimeTracking123!')
    db_host = os.getenv('DB_HOST', 'localhost') # Get the DB_HOST environment variable or use 'localhost' as default
    client = MongoClient(db_host, 27017, username='admin', password='TimeTracking123!')
    db = client.timetracking_db
    #TODO: Return Db if not none
    return db


"""
Checks the database connection
"""


def check_db_connection():
    # Check if the database connection is successful
    if client is None:
        return "Database connection not initialized"
    try:
        client.server_info()
        return "Connection successful"
    except Exception as e:
        return str(e)

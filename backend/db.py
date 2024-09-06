
"""
Author: Dominik Pollok, Phil Gengenbach, Alina Petri, José Ayala, Johann Kohl
Date: 2024-09-06
Description: Clockwise - Intuitive Time Tracking Web-App for Research Assistants
"""

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
    db_username = os.getenv('DB_USERNAME', 'admin') # Get the DB_USERNAME environment variable or use 'admin' as default
    db_password = os.getenv('DB_PASSWORD', 'TimeTracking123!') # Get the DB_PASSWORD environment variable or use 'TimeTracking123!' as default
    client = MongoClient(db_host, 27017, username=db_username, password=db_password) # Connect to the MongoDB server
    db = client.timetracking_db_production

    return db


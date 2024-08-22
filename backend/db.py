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
    client = MongoClient('158.180.40.137', 27017, username='admin', password='TimeTracking123!')
    #db = client.timetracking_db
    db = client.timetracking_user_doc_db
    #TODO: Return Db if not none
    return db


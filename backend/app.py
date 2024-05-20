from flask import Flask
from db import initialize_db

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"  # Database Connection

initialize_db(app)


@app.route('/')
def home():
    return "Flask Backend"


if __name__ == '__main__':
    app.run(debug=True)

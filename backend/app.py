from flask import Flask

app = Flask(__name__)


@app.route('/')
def home():
    return "Flask Backend"


if __name__ == '__main__':
    print("Test")
    app.run(debug=True)
